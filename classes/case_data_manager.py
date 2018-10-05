import sqlite3
from nameparser import HumanName
from functions.validate import (
    get_string,
    get_case_number,
    zip_find,
    menu_choice,
    get_integer
)


class CaseDataManager(object):
    # The __init__ function asks for a case number, queries the database to see
    # if the case number already exists, and assigns data if case does exist.
    # Then calls the update_case_data function on the old case data.
    # If not, sends us to the get_remaining_case_data to get what we need.
    def __init__(self, dbm):
        self.dbm = dbm
        self.case_number = get_case_number()
        sql = "SELECT * FROM CaseData WHERE CaseNumber = %s" % self.case_number
        case = self.dbm.query(sql)
        self.case_list = []
        for row in case:
            for item in row:
                self.case_list.append(item)
        if len(self.case_list) is 0:
            self.case_list.append(int(self.case_number))
            self.get_remaining_case_data(self.case_list)
        else:
            print "\nFound the case!"
            self.update_case_data()

    def print_case_data(self, types):
        # prints case data for active object
        # call using obj.print_case_data()
        for index, (type, item) in enumerate(zip(types, self.case_list)):
            print str(index+1).rjust(2) + ". " + str(type) + ": " + str(item)

    def update_case_data(self):
        # allows user the chance to update selected case data
        # called by __init__ if case number is exisiting in database
        column_names = self.dbm.get_column_names()
        while True:
            print "\n 0. Nothing more to update!"
            self.print_case_data(column_names)
            prompt = "Please select a line to update (or 0 if you're done)."
            line = menu_choice(prompt, str(range(len(self.case_list)+1)))
            if line is 0:
                break
            elif line is 1:
                print "You can't change the case number."
            else:
                prompt = "Replace data: %s" % self.case_list[line-1]
                if type(self.case_list[line-1]) is int:
                    self.case_list[line-1] = get_integer(prompt)
                else:
                    self.case_list[line-1] = get_string(prompt)
                self.dbm.amend_case_data(self.case_list, line-1)

    # Called by __init__
    def get_remaining_case_data(self, case_list):
            # START HELPER FUNCTIONS #
            # THESE FUNCTIONS CHECK FOR MATCHING EXISITING DATA FROM OTHER ROWS
        def check_for_respondent():
            sql = "SELECT %s FROM CaseData WHERE Respondent = %s LIMIT 1" % (
                "Respondent, Project, RespAddress, RespContact, RespCity, "
                "RespState, RespZip, RespEmail", "'" + self.resp_name + "'"
            )
            resp = self.dbm.query(sql)
            self.resp_list = []
            for row in resp:
                for item in row:
                    self.resp_list.append(item)

        def check_for_complainant():
            sql = "SELECT %s FROM CaseData WHERE CompName = %s LIMIT 1" % (
                "CompName, CompTitle, CompFirst, CompLast, CompAddress, "
                "CompCity, CompState, CompZip, CompEmail",
                "'" + self.comp_name + "'"
            )
            comp = self.dbm.query(sql)
            self.comp_list = []
            for row in comp:
                for item in row:
                    self.comp_list.append(item)
            # END HELPER FUNCTIONS #

        ### START get_remaining_case_data ###
        # # # Respondent and project info # # #
        self.resp_name = get_string("Enter respondent name.")

        # See if we can find the respondent in any other case in our database
        check_for_respondent()

        if len(self.resp_list) is 8:
            print "\nFound respondent in database! Assigning data..."
            for item in self.resp_list:
                self.case_list.append(item)
        else:
            self.case_list.append(self.resp_name)
            self.case_list.append(get_string("Enter project name."))
            self.case_list.append(get_string("Enter respondent address."))
            rc = get_string("Enter respondent contact with title.")
            self.case_list.append(rc)
            zip = zip_find("respondent").replace(",", "").split(" ")
            for z in zip:
                self.case_list.append(z) # city / state abbr / zip
            self.case_list.append(get_string("Enter respondent email."))

        # # # Complainant info # # #
        self.comp_name = get_string("Enter complainant name with title.")

        # See if we can find complainant in any other case in our database
        check_for_complainant()

        if len(self.comp_list) is 9:
            print "\nFound complainant in database! Assigning data..."
            for item in self.comp_list:
                self.case_list.append(item)
        else:
            self.case_list.append(self.comp_name)
            human_name = HumanName(self.comp_name)
            self.case_list.append(human_name['title'])
            self.case_list.append(human_name['first'])
            self.case_list.append(human_name['last'])
            self.case_list.append(get_string("Enter complainant address."))
            zip = zip_find("complainant").replace(",", "").split(" ")
            for z in zip:
                self.case_list.append(z) # city / state abbr / zip
            self.case_list.append(get_string("Enter complainant email."))

        # Now save our data into our database!
        try:
            self.dbm.insert_new_case_data(self.case_list)
        except sqlite3.IntegrityError as e:
            # this shouldn't actually be invoked, but just in case...
            print e, " ... case already exists!"
