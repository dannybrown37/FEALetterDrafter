import sqlite3
from classes.db_manager import DatabaseManager
from classes.case_data_manager import CaseDataManager
from classes.correspondence_manager import CorrespondenceManager
from classes.review_manager import ReviewManager
from classes.aeo_manager import AEOManager
from functions.validate import menu_choice
from functions.query_case import amend_table_data


def main():
    while True:
        # Chooseth the thing to doeth
        prompt = ("1. Draft a letter.\n"
                  "2. Update case data.\n"
                  "3. Query data and update any table in the database.\n"
                  "4. Get assistance with an initial review.\n"
                  "5. Create an AEO.\n"
                  "6. Delete case data from the database.\n"
                  "Q. (Exit the program.)\n")
        choice = menu_choice(prompt, "123456Qq")

        # Do the thing
        dbm = DatabaseManager("fea_case_data.db")
        if choice is 1:
            cdm = CaseDataManager(dbm)
            CorrespondenceManager(dbm, cdm)
        elif choice is 2:
            CaseDataManager(dbm)
        elif choice is 3:
            amend_table_data(dbm)
        elif choice is 4:
            cdm = CaseDataManager(dbm)
            ReviewManager(dbm, cdm)
        elif choice is 5:
            AEOManager()
        elif choice is 6:
            dbm.delete_case_data()
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
