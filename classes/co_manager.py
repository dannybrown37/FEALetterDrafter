import os
import datetime
import mailmerge # pip install docx-mailmerge
from functions.validate import (
    get_bool,
    get_string,
    get_integer,
    get_certified_mail_number,
    get_respondent_salutation,
    menu_choice,
    zip_find
)
from uszipcode import SearchEngine

class ConsentOrderManager(object):
    def __init__(self, dbm, cdm):
        self.dbm = dbm
        self.cdm = cdm
        self.get_merge_fields()
        self.generate_order()

    def get_merge_fields(self):
        self.merge_dict = {} # to hold our merge data we will collect

        # Different consent orders for different respondent types
        self.respondent_type = menu_choice(
            (
                "Select the respondent type:\n"
                "1. Association\n"
                "2. Developer\n"
            ),
            "12" # acceptable responses
        )

        # Make a list with all the documents we're creating
        root_folder = "admin_action_templates/"
        self.file_names = [
            root_folder + "COOL_Template.docx",
            root_folder + "CPW_Template.docx",
            root_folder + "InvestigativeReport_Template.docx"
        ]

        # Add either the association or developer CO per the above
        if self.respondent_type is 1:
            self.file_names.append(
                root_folder + "ConsentOrderAssociation_Template.docx"
            )
            self.respondent_type = "Association"
        elif self.respondent_type is 2:
            self.file_names.append(
                root_folder + "ConsentOrderDeveloper_Template.docx",
            )
            self.respondent_type = "Developer"

        # Now collect the merge field, fill information we already have,
        # and collect the info we don't already have
        for file_name in self.file_names:
            # First get the merge fields that are in the current document
            with mailmerge.MailMerge(file_name) as document:
                self.merge_fields = sorted(list(document.get_merge_fields()))

            # Then get the data for those fields
            for mf in self.merge_fields:
                # skip if we already have the data
                if mf in self.merge_dict:
                    continue
                    
                elif mf == "CondoCity" or mf == "CountyOfCondo":
                    zip = get_integer("What is the condo's zip code?")
                    search = SearchEngine()
                    data = search.by_zipcode(zip)
                    try:
                        self.merge_dict["CondoCity"] = data.city
                        self.merge_dict["CountyOfCondo"] = (
                            data.county.replace(" County", "")
                        )
                        print "City:", data.city, "|" , "County:", data.county
                    except AttributeError:
                        self.merge_dict["CondoCity"] = get_string(
                            "What is the CondoCity?"
                        )
                        self.merge_dict["CountyOfCondo"] = get_string(
                            "What is the CountyOfCondo?"
                        )

                elif mf == "Respondent":
                    self.merge_dict[mf] = self.cdm.case_list[1]
                elif mf == "Project":
                    self.merge_dict[mf] = self.cdm.case_list[2]
                elif mf == "RespondentAddress":
                    self.merge_dict[mf] = self.cdm.case_list[3]
                elif mf == "RespondentAddress2":
                    self.merge_dict[mf] = self.cdm.case_list[4]
                elif mf == "RespondentCityStateZip":
                    self.merge_dict[mf] = "%s, %s %s" % ( # respCityStateZip
                        self.cdm.case_list[5],
                        self.cdm.case_list[6],
                        self.cdm.case_list[7]
                    )
                elif mf == "RespondentEmail":
                    self.merge_dict[mf] = self.cdm.case_list[8]
                elif mf == "RespondentSalutation":
                    self.merge_dict[mf] = get_respondent_salutation(
                        self.cdm.case_list[4]
                    )
                elif mf == "Association":
                    # if respondent is association, we have that data
                    if self.respondent_type == "Association":
                        self.merge_dict[mf] = self.cdm.case_list[1]
                    # if respondent is developer, we need to clarify assoc name
                    elif self.respondent_type == "Developer":
                        self.merge_dict[mf] = get_string(
                            "What is the {}? ".format(mf)
                        )
                elif mf == "CaseNumber":
                    self.merge_dict[mf] = str(self.cdm.case_list[0])
                elif mf == "Condominium":
                    self.merge_dict[mf] = self.cdm.case_list[2]
                elif mf == "CertMailNumberForCOOL":
                    self.merge_dict[mf] = get_certified_mail_number()
                elif mf == "DateOfInvestigativeReport":
                    self.merge_dict[mf] = (
                        datetime.datetime.today().strftime('%B %d, %Y')
                    )
                elif mf == "NameOfComplainant":
                    self.merge_dict[mf] = (
                        self.cdm.case_list[9]
                    )
                elif mf == "RegisteredAgentCityStateZip":
                    self.merge_dict[mf] = zip_find("registered agent")
                else:
                    self.merge_dict[mf] = get_string(
                        "What is the {}? ".format(mf)
                    )

    def generate_order(self):
        for file_name in self.file_names:
            script_dir = os.path.dirname("main.py")
            absolute_path = os.path.join(script_dir, file_name)
            document = mailmerge.MailMerge(absolute_path)
            document.merge(**self.merge_dict)
            output_name = file_name.replace(
                "admin_action_templates/", "").replace("_Template", "")
            output_path = os.path.join(
                script_dir,
                "{} {}".format(self.cdm.case_list[0], output_name)
            )
            document.write(output_path)
            print "\nYour {} has been generated!".format(output_name)
