import sqlite3
from classes.db_manager import DatabaseManager
from classes.case_data_manager import CaseDataManager
from classes.correspondence_manager import CorrespondenceManager
from classes.review_manager import ReviewManager
from classes.aeo_manager import AEOManager
from classes.co_manager import ConsentOrderManager
from classes.closing_manager import ClosingManager
from classes.annual_financials_review_manager import AFReviewManager
from classes.budget_review_manager import BudgetReviewManager
from functions.validate import menu_choice
from functions.query_case import amend_table_data
from functions.query_table import query_entire_table


def main():

    while True:
        # Chooseth the thing to doeth
        prompt = ("1. Draft a letter.\n"
                  "2. Draft a Consent Order (and related documents).\n"
                  "3. Create an AEO.\n"
                  "4. Get assistance with an initial review.\n"
                  "5. Get assistance with case closing procedures.\n"
                  "6. Get assistance reviewing annual financials.\n"
                  "7. Get assistance reviewing a budget and reserve schedule."
                  "\n\n"
                  "Q. (Exit the program.)\n")
        choice = menu_choice(prompt, "1234567Qq")

        # Do the thing
        dbm = DatabaseManager("fea_case_data.db")

        if choice is 1:
            cdm = CaseDataManager(dbm)
            CorrespondenceManager(dbm, cdm)
        elif choice is 2:
            cdm = CaseDataManager(dbm)
            ConsentOrderManager(dbm, cdm)
        elif choice is 3:
            AEOManager()
        elif choice is 4:
            cdm = CaseDataManager(dbm)
            ReviewManager(dbm, cdm)
        elif choice is 5:
            cdm = CaseDataManager(dbm)
            ClosingManager(dbm, cdm)
        elif choice is 6:
            AFReviewManager()
        elif choice is 7:
            BudgetReviewManager()
        elif choice.lower() == "q":
            exit()


if __name__ == '__main__':
    main()

"""
# Useful stuff to copy/paste

dummy = [2018021031, "RESP", "PROJ", "RESPADDRESS", "RESPCONTACT", "RESPCITY",
        "RESPSTATE", 32048, "RESPEMAIL", "COMPNAME", "COMPTITLE", "COMPFIRST",
        "COMPLAST", "COMPADDRESS", "COMPCITY", "COMPSTATE", 32309, "COMPEMAIL"]
dbm.insert_new_case_data(dummy)

dbm.drop_table("")
dbm.create_table("")
dbm.drop_table("ImportantDates")
dbm.create_table("ImportantDates")
dbm.drop_table("CaseData")
dbm.create_table("CaseData")
dbm.drop_table("LetterTypes")
dbm.create_table("LetterTypes")

dbm.drop_table("AppraiserSites")
dbm.create_table("AppraiserSites")
"""

"""
# May want to bring these back at some point? Not always relevant
"Database Maintenance Options\n"
" 8. Update case data.\n"
" 9. Query and update data in any table in the database.\n"
"10. Query an entire table and print the results.\n"
"11. Delete case data from the database.\n"
"\n"
"""

"""
elif choice is 8:
    CaseDataManager(dbm)
elif choice is 9:
    amend_table_data(dbm)
elif choice == 10:
    query_entire_table(dbm)
elif choice == 11:
    dbm.delete_case_data()
"""
