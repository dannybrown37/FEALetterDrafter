import sqlite3
from db_manager import DatabaseManager
from case_data_manager import CaseDataManager
from validate import get_case_number

dummy = [2018021031, "RESP", "PROJ", "RESPADDRESS", "RESPCONTACT", "RESPCITY",
        "RESPSTATE", 32048, "RESPEMAIL", "COMPNAME", "COMPTITLE", "COMPFIRST",
        "COMPLAST", "COMPADDRESS", "COMPCITY", "COMPSTATE", 32309, "COMPEMAIL"]

def main():
    dbm = DatabaseManager("fea_case_data.db")
    cd = CaseDataManager(dbm)





if __name__ == '__main__':
    main()



"""
# Potentially useful stuff for cut/paste

dbm.insert_new_case_data(dummy)
dbm.delete_case_data(2018021031)
dbm.create_table("CaseData")
dbm.drop_table("CaseData")

results = dbm.query('select * from casedata where CaseNumber = 2018021031')
for result in results:
    print result



cd.print_case_data()

"""
