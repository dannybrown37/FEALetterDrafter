from functions.validate import menu_choice, get_string, get_due_date


class CorrespondenceManager(object):
    # This manager gets the data specific to letters and then creates them.
    def __init__(self, dbm, cdm):
        self.dbm = dbm
        self.cdm = cdm
        self.case_data_categories = self.dbm.get_column_names()
        self.dbm.query("SELECT * FROM LetterTypes")
        self.letter_types = self.dbm.get_column_names()
        self.letter_types.pop(0) # remove the CaseNumber column
        self.to_gen = []
        # populate values in to_gen for letters to create
        print " 0. I'm done selecting letters to generate!"
        for index, type in enumerate(self.letter_types):
            print str(index+1).rjust(2) + ". " + type
        prompt = "Select a letter to generate (or 0 if done selecting)."
        choices = str(range(len(self.letter_types)+1))
        self.to_gen.append(menu_choice(prompt, choices))
        while self.to_gen[-1] is not 0:
            print "Letters selected so far: %s" % self.to_gen
            self.to_gen.append(menu_choice(prompt, choices))
        self.to_gen.pop() # remove the last selection of 0
        for i in range(len(self.to_gen)): # set to actual indexes
            self.to_gen[i] = self.to_gen[i] - 1 # (by subtracting one)
        self.closing_no_contact_ackc()

    def ackc(self):
        prompt = "What phone number did you try for complainant?"
        self.comp_phone = get_string(prompt)
        self.first_call = get_string("What was the date of your first call?")
        self.second_call = get_string("What was the date of your second call?")
        self.ackc_due = get_due_date("ACKC")

    def closing_no_contact_ackc(self):
        case_num = self.cdm.case_list[0]
        sql = "SELECT ACKC FROM LetterTypes WHERE CaseNumber = %s" % case_num
        date = self.dbm.query(sql)
        # TODO debug this, consider putting into a more reusable function
