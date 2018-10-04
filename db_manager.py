import sqlite3


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
        self.cursor.execute(
            '''
            INSERT INTO CaseData
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''',
            case_list
        )
        self.connection.commit()

    def delete_case_data(self, case_number):
        # deletes a row with matching case number
        # to use, call with obj.delete_case_data(case_number)
        sql = ''' DELETE FROM CaseData WHERE CaseNumber = ? '''
        self.cursor.execute(sql, (case_number,))


    def table_creation(self):
        # Creates table for basic case data // as of 10-04-2018
        try:
            self.cursor.execute(
                'CREATE TABLE CaseData ('
                    'CaseNumber INTEGER PRIMARY KEY,'
                    'Respondent TEXT,'
                    'Project TEXT,'
                    'RespAddress TEXT,'
                    'RespContact TEXT,'
                    'RespCity TEXT,'
                    'RespState TEXT,'
                    'RespZip INTEGER,'
                    'RespEmail TEXT,'
                    'CompTitle TEXT,'
                    'CompFirst TEXT,'
                    'CompLast TEXT,'
                    'CompAddress TEXT,'
                    'CompCity TEXT,'
                    'CompState TEXT,'
                    'CompZip INTEGER,'
                    'CompEmail TEXT'
                ')'
            )
        except sqlite3.OperationalError as e:
            print e, " ... skipping creation"

        # Creates table for important dates // as of 10-04-2018
        try:
            self.cursor.execute(
                'CREATE TABLE ImportantDates ('
                    'CaseNumber INTEGER PRIMARY KEY,'
                    'ACKCDueDate TEXT,'
                    'CCCLReqEvDueDate TEXT,'
                    'ALGLDueDate TEXT,'
                    'WLDueDate TEXT,'
                    'DateOfACKC TEXT,'
                    'DateOfCTC TEXT,'
                    'DateOfCCCL TEXT,'
                    'DateOfWL TEXT'
                ')'
            )
        except sqlite3.OperationalError as e:
            print e, " ... skipping creation"
