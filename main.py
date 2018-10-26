import sqlite3
from classes.db_manager import DatabaseManager
from classes.case_data_manager import CaseDataManager
from classes.correspondence_manager import CorrespondenceManager
from functions.validate import menu_choice
from functions.query_case import query_case


def main():
    dbm = DatabaseManager("fea_case_data.db")
    prompt = ("1. Draft a letter.\n"
              "2. Update case data.\n"
              "3. Query the database.")
    choice = menu_choice(prompt, "123")

    if choice is 1:
        cdm = CaseDataManager(dbm)
        CorrespondenceManager(dbm, cdm)
    elif choice is 2:
        CaseDataManager(dbm)
    elif choice is 3:
        query_case(dbm)

if __name__ == '__main__':
    main()

"""
# Useful stuff to copy/paste

dbm.delete_case_data(2018021031)

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

results = dbm.query('select * from CaseData')
for result in results:
    print result
results = dbm.query('select * from ImportantDates')
for result in results:
    print result
results = dbm.query('select * from LetterTypes')
for result in results:
    print result

results = dbm.query('select * from casedata where CaseNumber = 2018021031')
for result in results:
    print result

results = dbm.query('select * from importantdates where CaseNumber = 2018021031')
for result in results:
    print result


cd.print_case_data()

"""
