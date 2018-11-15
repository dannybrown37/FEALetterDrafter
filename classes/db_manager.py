import sqlite3
from functions.validate import get_case_number


class DatabaseManager(object):
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.connection.commit()
        self.cursor = self.connection.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor
        # to print results, assign return to var and then use a for loop

    def __del__(self):
        self.connection.close()

    def insert_new_case_data(self, case_list):
        # inserts a new row using a list of case data
        # to use, call with obj.insert_new_case_data(case_list)
        case_number_in_list = [case_list[0]]
        sql = """ INSERT INTO CaseData
                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
        self.cursor.execute(sql, case_list) # self.query doesn't work here
        sql = """ INSERT INTO ImportantDates
                  VALUES (?, NULL, NULL, NULL, NULL, NULL) """
        self.cursor.execute(sql, case_number_in_list)
        sql = """ INSERT INTO LetterTypes
                  VALUES (
                      ? , NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                      NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
                  ) """
        self.cursor.execute(sql, case_number_in_list)
        self.connection.commit()

    def insert_appraiser_website(self, county, website):
        # Won't likely be used once we've populated this data
        sql = """ INSERT INTO AppraiserSites
                  VALUES (?, ?) """
        self.cursor.execute(sql, [county, website])
        self.connection.commit()
        results = self.query('SELECT * From AppraiserSites')

    def query_important_date(self, date_type, case_number):
        # returns a specific date from a specific case as specified
        sql = "SELECT %s FROM ImportantDates WHERE CaseNumber = %s" % (
            date_type, case_number
        )
        return self.query(sql)

    def amend_important_date(self, column_name, date, case_number):
        # saves a specific
        sql = "UPDATE ImportantDates SET %s = '%s' WHERE %s = %s" % (
            column_name, date, "CaseNumber", case_number
        )
        self.query(sql)

    def amend_case_data(self, case_list, index):
        column_names = self.get_column_names()
        print column_names[index]
        print case_list[index]
        sql = "UPDATE CaseData SET %s = '%s' WHERE %s = %s" % (
            column_names[index], case_list[index], "CaseNumber", case_list[0]
        )
        self.query(sql)

    def delete_case_data(self):
        # deletes a row with matching case number
        print "\nYou've chosen to delete case data!"
        case = get_case_number()

        # Verify the table actually exists
        q = self.query("SELECT * FROM CaseData WHERE CaseNumber = %s" % case)
        count = []
        for row in q:
            for item in row:
                count.append(item)
        if len(count) is 0:
            print "\nThe table does not exist!"
            return # Go back to main if the case does not exist

        # If the case exists, we can delete all the rows associated with it
        tables = ['CaseData', 'ImportantDates', 'LetterTypes']
        for table_name in tables: # self.query doesn't work here because of ?
            sql = """ DELETE FROM %s WHERE CaseNumber = ? """ % table_name
            self.cursor.execute(sql, (case_number,))
        self.connection.commit()

    def get_column_names(self):
        return [description[0] for description in self.cursor.description]

    def drop_table(self, table_name):
        # drops specified table
        try:
            sql = 'DROP TABLE %s' % table_name
            self.cursor.execute(sql)
            print "Table %s dropped!" % table_name
        except sqlite3.OperationalError as e:
            print e, " ... can't delete"

    def create_table(self, table_name):
        # Creates table for basic case data // as of 10-04-2018
        if table_name == "CaseData":
            try:
                self.cursor.execute(
                    """
                    CREATE TABLE CaseData (
                        CaseNumber INTEGER PRIMARY KEY,
                        Respondent TEXT,
                        Project TEXT,
                        RespAddress TEXT,
                        RespContact TEXT,
                        RespCity TEXT,
                        RespState TEXT,
                        RespZip INTEGER,
                        RespEmail TEXT,
                        CompName TEXT,
                        CompTitle TEXT,
                        CompFirst TEXT,
                        CompLast TEXT,
                        CompAddress TEXT,
                        CompCity TEXT,
                        CompState TEXT,
                        CompZip INTEGER,
                        CompEmail TEXT
                    )
                    """
                )
                print "Table %s created!" % table_name
            except sqlite3.OperationalError as e:
                print e, " ... skipping creation"

        # Creates table for important dates // as of 10-04-2018
        if table_name == "ImportantDates":
            # This tracks data other than dates letters sent
            try:
                self.cursor.execute(
                    """
                    CREATE TABLE ImportantDates (
                        CaseNumber INTEGER PRIMARY KEY,
                        ACKCDueDate TEXT,
                        CCCLReqEvDueDate TEXT,
                        ALGLDueDate TEXT,
                        WLDueDate TEXT,
                        DateOfCTC TEXT
                    )
                    """
                )
                print "Table %s created!" % table_name
            except sqlite3.OperationalError as e:
                print e, " ... skipping creation"

        # Creates table for letter types and (approximate) dates sent
        if table_name == "LetterTypes":
            # This can be used to track the dates a letter was sent
            try:
                self.cursor.execute(
                    """
                    CREATE TABLE LetterTypes (
                        CaseNumber INTEGER PRIMARY KEY,
                        ACKC TEXT,
                        ClosingNoContactACKC TEXT,
                        CCCL TEXT,
                        CCCLClosingNJ TEXT,
                        CCCLClosingCCD TEXT,
                        CCCLRequestingEvidence TEXT,
                        ClosingLOD TEXT,
                        Allegation TEXT,
                        Information TEXT,
                        Warning TEXT,
                        WarningInformation TEXT,
                        ClosingCompViolation TEXT,
                        ClosingRespViolation TEXT,
                        ClosingCompNoViolation TEXT,
                        ClosingRespNoViolation TEXT,
                        PSTU TEXT
                    )
                    """
                )
                print "Table %s created!" % table_name
            except sqlite3.OperationalError as e:
                print e, " ... skipping creation"

        if table_name == "AppraiserSites":
            # This will be used to hold the county property appraiser sites
            try:
                self.cursor.execute(
                    """
                    CREATE TABLE AppraiserSites (
                        County TEXT PRIMARY KEY,
                        Site TEXT
                    )
                    """
                )
                print "Tables %s created!" % table_name
            except sqlite3.OperationalError as e:
                print e, " ... skipping creation"
