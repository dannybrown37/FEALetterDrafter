import os
import glob
from mailmerge import MailMerge # pip install docx-mailmerge
from functions.validate import (
    menu_choice,
    get_string,
    get_due_date,
    get_respondent_salutation,
    get_certified_mail_number
)


class CorrespondenceManager(object):
    # This manager gets the data specific to letters and then creates them.
    def __init__(self, dbm, cdm):
        self.dbm = dbm
        self.cdm = cdm
        self.dbm.query("SELECT * FROM CaseData") # needed for next line
        self.case_data_categories = self.dbm.get_column_names()
        self.dbm.query("SELECT * FROM LetterTypes") # needed for next line
        self.letter_types = self.dbm.get_column_names()
        self.letter_types.pop(0) # remove the CaseNumber column
        self.to_gen = []
        # populate values in to_gen for letters to create
        print " 0. I'm done selecting letters to generate!"
        for index, type in enumerate(self.letter_types):
            print str(index+1).rjust(2) + ". " + type
        prompt = "Select a letter to generate (or 0 if done selecting)."
        choices = str(range(len(self.letter_types)+1))
        self.to_gen.append(menu_choice(prompt, choices))
        while self.to_gen[-1] is not 0:
            print "Letters selected so far: %s" % self.to_gen
            self.to_gen.append(menu_choice(prompt, choices))
        self.to_gen.pop() # remove the last selection of 0
        for i in range(len(self.to_gen)): # set to actual indexes
            self.to_gen[i] = self.to_gen[i] - 1 # (by subtracting one)
        self.letter_type_names = []
        for num in self.to_gen:
            self.letter_type_names.append(self.letter_types[num])
        self.merge_fields = self.get_merge_fields_from_selected_letters()
        self.get_merge_field_data()
        self.generate_letter()

    def generate_letter(self):
        script_dir = os.path.dirname("main.py")
        for letter_type in self.letter_type_names:
            absolute_path = os.path.join(
                script_dir,
                "letter_templates/%s_Template.docx" % letter_type
            )
            document = MailMerge(absolute_path)
            document.merge(
                caseNumber = str(self.case_number),
                certMailNumber = self.cert_mail_number,
                # Complainant data
                complainant = self.complainant,
                compAddress = self.comp_address,
                compCityStateZip = self.comp_csz,
                compEmail = self.comp_email,
                compSalutation = self.comp_salutation,
                # Respondent data
                respondent = self.respondent,
                project = self.project,
                respAddress1 = self.resp_address,
                respAddress2 = self.resp_contact,
                respCityStateZip = self.resp_csz,
                respEmail = self.resp_email,
                respSalutation = self.resp_salutation,
                # Allegations and evidence
                allegations = self.allegations,
                evidence = self.evidence,
                # ACKC data
                compPhone = self.comp_phone,
                call1date = self.first_call,
                call2date = self.second_call,
                # Dates
                dueDateACKC = self.due_date_ackc,
                dueDateCCCLReqEv = self.due_date_cccl,
                dueDateAllegation = self.due_date_algl,
                dueDateWarning = self.due_date_wl,
                dateOfCTC = self.date_of_ctc,
                ILCallDate = self.il_call_date,
                # Need to do (approximate) date of letter sending
                # TODO dateOfCCCL,
                # TODO dateOfACKC,
                # TODO dateOfWL,
            )
            output_absolute_path = os.path.join(
                script_dir,
                "%s %s %s.docx" % (self.case_number, self.project, letter_type)
            )
            document.write(output_absolute_path)
            print "\nYour %s has been generated!" % letter_type


    def get_merge_field_data(self):                     # Merge variable name:
        # Assigning these for clarity only
        self.case_number = self.cdm.case_list[0]        # caseNumber
        self.respondent = self.cdm.case_list[1]         # respondent
        self.project = self.cdm.case_list[2]            # project
        self.resp_address = self.cdm.case_list[3]       # respAddress1
        self.resp_contact = self.cdm.case_list[4]       # respAddress2
        self.resp_csz = "%s, %s %s" % (                 # respCityStateZip
            self.cdm.case_list[5],
            self.cdm.case_list[6],
            self.cdm.case_list[7]
        )
        self.resp_email = self.cdm.case_list[8]         # respEmail
        self.complainant = self.cdm.case_list[9]        # complainant
        self.comp_salutation = '%s %s' % (              # compSalutation
            self.cdm.case_list[10],
            self.cdm.case_list[12]
        )
        self.comp_address = self.cdm.case_list[13]      # compAddress
        self.comp_csz = "%s, %s %s" % (                 # compCityStateZip
            self.cdm.case_list[14],
            self.cdm.case_list[15],
            self.cdm.case_list[16]
        )
        self.comp_email = self.cdm.case_list[17]        # compEmail
        #######################################################################

        # Important dates get their own sub-section
        def important_date_subquery(date_type): # Takes DB column name
            q = self.dbm.query_important_date(date_type, self.case_number)
            return q.fetchone()[0]

        def get_and_save_due_date(date_type): # Takes DB column name
            date = get_due_date(date_type.replace("DueDate", ""))
            self.dbm.amend_important_date(date_type, date, self.case_number)
            return date

        if "dueDateACKC" in self.merge_fields: # this is the merge variable name
            self.due_date_ackc = important_date_subquery("ACKCDueDate")
            if self.due_date_ackc is None:
                self.due_date_ackc = get_and_save_due_date("ACKCDueDate")
        else:
            self.due_date_ackc = None

        if "dueDateCCCLReqEv" in self.merge_fields: # this is the merge variable name
            self.due_date_cccl = important_date_subquery("CCCLReqEvDueDate")
            if self.due_date_cccl is None:
                self.due_date_cccl = get_and_save_due_date("CCCLReqEvDueDate")
        else:
            self.due_date_cccl = None

        if "dueDateAllegation" in self.merge_fields: # this is the merge variable name
            self.due_date_algl = important_date_subquery("ALGLDueDate")
            if self.due_date_algl is None:
                self.due_date_algl = get_and_save_due_date("ALGLDueDate")
        else:
            self.due_date_algl = None

        # this will grab WL/IL too
        if "dueDateWarning" in self.merge_fields: # this is the merge variable name
            self.due_date_wl = important_date_subquery("WLDueDate")
            if self.due_date_wl is None:
                self.due_date_wl = get_and_save_due_date("WLDueDate")
        else:
            self.due_date_wl = None

        if "dateOfCTC" in self.merge_fields:
            self.date_of_ctc = important_date_subquery("DateOfCTC")
            if self.date_of_ctc is None:
                self.date_of_ctc = get_string("What was the date of CTC?")
                self.dbm.amend_important_date(
                    "DateOfCTC", self.date_of_ctc, self.case_number)
        else:
            self.date_of_ctc = None

        # Info for complainant letters
        if "compPhone" in self.merge_fields:
            prompt = "What phone number did you try for complainant?"
            self.comp_phone = get_string(prompt)
        else:
            self.comp_phone = None

        if "call1date" and "call2date" in self.merge_fields:
            self.first_call = get_string("What date was your first call?")
            self.second_call = get_string("What date was your second call?")
        else:
            self.first_call, self.second_call = None, None

        # Info for respondent letters
        if "respSalutation" in self.merge_fields:
            self.resp_salutation = get_respondent_salutation(self.resp_contact)
        else:
            self.resp_salutation = None

        if "certMailNumber" in self.merge_fields:
            self.cert_mail_number = get_certified_mail_number()
        else:
            self.cert_mail_number = None

        if "ILCallDate" in self.merge_fields:
            self.il_call_date = get_string("What was the IL call date?")
        else:
            self.il_call_date = None

        # Self-filling allegations/evidence get their own sub-sections
        self.allegations = None
        self.evidence = None
        # TODO add this functionality

    def get_merge_fields_from_selected_letters(self):
        master_list = []
        for n in self.letter_type_names:
            for file_name in glob.glob("letter_templates/%s_Template.docx" % n):
                with MailMerge(file_name) as document:
                    merge_fields = list(document.get_merge_fields())
                    for mf in merge_fields:
                        if mf not in master_list:
                            master_list.append(mf)
        return master_list

    def get_merge_fields_from_all_letters(self):
        # This was just a helper function to get a list of all merge fields
        # Will be useful again should major revisions or additions happen with
        # letters. It could be combined with the above but whatever.
        master_list = []
        for file_name in glob.glob("letter_templates/*.docx"):
            with MailMerge(file_name) as document:
                merge_fields = list(document.get_merge_fields()) # COOL FUNCTION
                for mf in merge_fields:
                    if mf not in master_list:
                        master_list.append(mf)
                """
                # This can check for undesirable mfs we wish to remove
                if 'dueDate' in merge_fields:
                    print file_name
                """
        print master_list
        """ # As of 10/05/2018
        ['complainant', 'compCityStateZip', 'caseNumber', 'compSalutation',
        'dueDateACKC', 'compAddress', 'compPhone', 'call2date', 'project',
        'call1date', 'respondent', 'dueDateAllegation', 'respAddress1',
        'allegations', 'respSalutation', 'respAddress2', 'respCityStateZip',
        'certMailNumber', 'respEmail', 'evidence', 'dateOfCTC', 'compEmail',
        'dueDateCCCLReqEv', 'dateOfCCCL', 'dateOfACKC', 'dateOfWL',
        'ILCallDate', 'dueDateWarning']
        """
