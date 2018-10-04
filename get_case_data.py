from nameparser import HumanName
from validate import get_string, get_case_number, zip_find


class GetCaseData(object):
    # The __init__ function asks for a case number, queries the database to see
    # if the case number already exists, and assigns data if case does exist.
    # If not, sends us to the get_remaining_case_data to get what we need.
    def __init__(self, dbm):
        self.case_number = get_case_number()
        sql = "SELECT * FROM CaseData WHERE CaseNumber = %s" % self.case_number
        case = dbm.query(sql)
        self.case_list = []
        for row in case:
            for item in row:
                self.case_list.append(item)
        if len(self.case_list) is 0:
            self.case_list.append(int(self.case_number))
            self.get_remaining_case_data(self.case_list)

    def print_case_data(self):
        print "\nData for case number %s:\n" % self.case_list[0]
        for item in self.case_list:
            print item

    def get_remaining_case_data(self, case_list):
        # Respondent and project info
        self.case_list.append(get_string("Enter respondent name."))
        self.case_list.append(get_string("Enter project name."))
        self.case_list.append(get_string("Enter respondent address."))
        self.case_list.append(get_string("Enter respondent contact with title."))
        zip = zip_find("respondent").replace(",", "").split(" ")
        self.case_list.append(zip[0]) # city
        self.case_list.append(zip[1]) # state
        self.case_list.append(zip[2]) # zip
        self.case_list.append(get_string("Enter respondent email."))

        # Complainant info
        name = HumanName(get_string("Enter complainant name with title."))
        self.case_list.append(name['title'])
        self.case_list.append(name['first'])
        self.case_list.append(name['last'])
        self.case_list.append(get_string("Enter complainant address."))
        zip = zip_find("complainant").replace(",", "").split(" ")
        self.case_list.append(zip[0]) # city
        self.case_list.append(zip[1]) # state
        self.case_list.append(zip[2]) # zip
        self.case_list.append(get_string("Enter complainant email."))

        print self.case_list
