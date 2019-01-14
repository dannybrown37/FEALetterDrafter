from .aeo_manager import AEOManager
import os
import datetime
import webbrowser as wb
import uszipcode
import subprocess
import mailmerge
import subprocess
from shutil import copy2
from uszipcode import SearchEngine
from functions.validate import get_string, get_bool, get_integer


class ReviewManager(object):
    def __init__(self, dbm, cdm):
        self.dbm = dbm
        self.cdm = cdm
        self.get_corporate_info()
        self.get_fees_info()
        self.get_ownership_info()
        self.generate_summary()
        AEOManager(self.cdm.case_list)
        self.generate_initial_checklist()
        # TODO add dialogue box on where to save? Figure out how to handle these

    def get_corporate_info(self):
        print "Corporation:", self.cdm.case_list[1]
        sunbiz = "http://search.sunbiz.org/Inquiry/CorporationSearch/ByName"
        wb.open_new_tab(sunbiz)
        self.corp_status = get_bool("Is corporate status active?")
        self.corp_status = "active" if self.corp_status is True else "inactive"

    def get_fees_info(self):
        print "Case Number:", self.cdm.case_list[0]
        vr = "http://vr:9029/le5/faces/jsp/VrDashboard.jsp"
        wb.open_new_tab(vr)
        self.num_of_units = get_integer("What is the number of units?")
        self.fees_paid = get_bool("Are all fees that are due paid?")
        self.fees_paid = "paid" if self.fees_paid is True else "not paid"

    def get_ownership_info(self):
        print "Owner:",  self.cdm.case_list[-9] # complainant name to search for
        zip = self.cdm.case_list[-2] # gets complainant zip code
        search = SearchEngine()
        data = search.by_zipcode(zip)
        # Get comp county; if not in Florida (or our list, ask for it manually)
        if data.state != "FL":
            print "The complainant lives in %s, not Florida." % data.state
            zip = self.cdm.case_list[7] # try the respondent instead of comp
            data = search.by_zipcode(zip)
            if data.state != "FL":
                print "The respondent is not in FL, either."
                county = get_string("In what county is the unit located?")
                county = county.title().replace("County", "").strip()
            else:
                county = data.county.replace("County", "").strip()
        else:
            county = data.county.replace("County", "").strip()
        # Get the list of counties from the AppraiserSites table
        results = self.dbm.query("SELECT * FROM AppraiserSites")
        counties = [result[0] for result in results]
        if county not in counties:
            print "%s not found in the list of counties." % county
            county = get_string("In what county is the unit located?")
            county = county.title().replace("County", "").strip()
        sql = " SELECT Site From AppraiserSites WHERE County =  '%s' " % county
        results = self.dbm.query(sql)
        appraiser_site = results.fetchone()[0]
        wb.open_new_tab(appraiser_site)
        self.owner = get_bool("Is complainant a unit owner?")
        self.owner = "unit owner" if self.owner is True else "not unit owner"

    def generate_summary(self):
        # Combine respondent and project names for easier comparison
        both = self.cdm.case_list[1].lower() + self.cdm.case_list[2].lower()
        # Determine project type
        if "condo" in both:
            self.project_type = "8002 condo"
        elif "coop" in both or "co-op" in both or "cooperative" in both:
            self.project_type = "8004 cooperative"
        else:
            self.project_type = get_string("What is the project type?")
        print ("\n[complainant is %s, project is %s, %s units, fees %s,"
               " corp status %s]") % (self.owner, self.project_type,
                        self.num_of_units, self.fees_paid, self.corp_status)

    def generate_initial_checklist(self):
        wait = get_string( # this doesn't do anything; just a reminder
            "Press enter to confirm allegations are entered in Versa."
        )
        # This is where we actually generate our checklist
        self.file_name = "checklists/2018 Case Opening Checklist.docx"

        merge_dict = { # These are the ones we know
            "Respondent" : self.cdm.case_list[1],
            "CaseNumber" : str(self.cdm.case_list[0]),
        }

        # Then we collect other data from the user
        merge_dict["DateReceived"] = get_string(
            "What was the date of receipt for the complaint? "
        )
        merge_dict["DateAssigned"] = get_string(
            "What was the date case was assigned to investigator?"
        )
        date = datetime.datetime.today().strftime('%m-%d-%Y')
        initials = get_string("What are your initials? ")
        merge_dict["InitialsAndDate"] = "%s %s" % (initials, date)

        # We've got our data, let's generate the document
        script_dir = os.path.dirname("main.py")
        absolute_path = os.path.join(script_dir, self.file_name)
        document = mailmerge.MailMerge(absolute_path)
        document.merge(**merge_dict)
        output_path = os.path.join(
            script_dir,
            "%s Initial Checklist.docx" % self.cdm.case_list[0]
        )
        document.write(output_path)

        # Open the new document to remind to index
        subprocess.Popen([output_path], shell=True)


    ##################################### Helper functions
    def populate_appraiser_websites(self):
        # Currently not called, as data is already collected.
        # This is just a helper function to put in all the exact owner search
        # sites for future use.
        # TODO: May want to add functionality that checks database for exisiting
        # data, should we want to update later with only some counties. Maybe.

        # We can add single data by just redefining counties to include specific
        # Use with -- self.populate_appraiser_websites()
        counties = [
            "Alachua", "Baker", "Bay", "Bradford", "Brevard", "Broward",
            "Calhoun", "Charlotte", "Citrus", "Clay", "Collier", "Columbia",
            "DeSoto", "Dixie", "Duval", "Escambia", "Flagler", "Franklin",
            "Gadsden", "Gilchrist", "Glades", "Gulf", "Hamilton", "Hardee",
            "Hendry", "Hernando", "Highlands", "Hillsborough", "Holmes",
            "Indian River", "Jackson", "Jefferson", "Lafayette", "Lake", "Lee",
            "Leon", "Levy", "Liberty", "Madison", "Manatee", "Marion", "Martin",
            "Miami-Dade", "Monroe", "Nassau", "Okaloosa", "Okeechobee",
            "Orange", "Osceola", "Palm Beach", "Pasco", "Pinellas", "Polk",
            "Putnam", "St. Johns", "St. Lucie", "Santa Rosa", "Sarasota",
            "Seminole", "Sumter", "Suwannee", "Taylor", "Union", "Volusia",
            "Wakulla", "Walton", "Washington"
        ]
        for county in counties:
            search_term = "%s+county+property+appraiser" % county
            wb.open_new_tab("google.com/search?q=%s" % search_term)
            website = raw_input("Enter the website for %s: " % county)
            self.dbm.insert_appraiser_website(county, website)
