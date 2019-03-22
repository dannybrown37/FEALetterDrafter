import os
import mailmerge
import datetime
import dateparser
import subprocess
from functions.validate import get_string, get_bool


class ClosingManager(object):
    def __init__(self, dbm, cdm):
        self.dbm = dbm
        self.cdm = cdm
        self.file_name = "checklists/2018 Case Closing Checklist.docx"
        self.get_merge_data()
        self.generate_closing_checklist()

    def get_merge_data(self):
        # This is the data we have already, no need to recollect it
        self.merge_dict = {
            "CaseNumber" : str(self.cdm.case_list[0]),
            "Complainant" : self.cdm.case_list[9],
            "Respondent" : self.cdm.case_list[1],
            "Date" : datetime.datetime.today().strftime('%m-%d-%Y')
        }

        # Here is the data we do need to collect
        self.merge_dict["DateCaseOpened"] = get_string(
            "What was the date the case was opened?"
        )

        self.merge_dict["RelatedCaseNumbers"] = get_string(
            "If applicable, add a comma-separated list of related case numbers."
        )

        # We can operate logic on whether PSTUs should have been completed
        opened = dateparser.parse(self.merge_dict["DateCaseOpened"])
        today = datetime.datetime.today()
        num_days = today - opened
        num_days = num_days.days # gives us just the number of days as an int

        # Now this won't fire if case has been opened for less than 90 days
        # If it has been open for more than 90, will confirm each required PSTU
        for x in range(90, num_days, 30):
            if get_bool("Enter true/yes/1 to confirm a %s-day PSTU." % x):
                self.merge_dict["%sDayPSTU" % x] = self.merge_dict["Date"]
            else:
                self.merge_dict["%sDayPSTU" % x] = None

    def generate_closing_checklist(self):
        wait = get_string( # this doesn't do anything; just a reminder
            "Press enter to confirm allegation dispositions are entered "
            "in Versa."
        )
        script_dir = os.path.dirname("main.py")
        absolute_path = os.path.join(script_dir, self.file_name)
        document = mailmerge.MailMerge(absolute_path)
        document.merge(**self.merge_dict)
        output_path = os.path.join(
            script_dir,
            "{} Closing Checklist.docx".format(self.cdm.case_list[0])
        )
        document.write(output_path)

        # Open the new document to remind to index
        subprocess.Popen([output_path], shell=True)
