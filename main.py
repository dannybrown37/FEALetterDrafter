import sqlite3
from classes.db_manager import DatabaseManager
from classes.case_data_manager import CaseDataManager
from classes.correspondence_manager import CorrespondenceManager




def main():
    dbm = DatabaseManager("fea_case_data.db")
    cdm = CaseDataManager(dbm)
    cor = CorrespondenceManager(dbm, cdm)







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
