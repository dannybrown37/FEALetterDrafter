from functions.validate import get_certified_mail_number, menu_choice


class CorrespondenceManager(object):
    # This manager gets the data specific to letters and then creates them.
    def __init__(self, dbm, cdm):
        self.dbm = dbm
        self.dbm.query("SELECT * FROM LetterTypes")
        self.letter_types = self.dbm.get_column_names()
        self.cdm = cdm
        self.to_gen = []
        while True:
            print " 0. I'm done selecting letters to generate!"
            for index, type in enumerate(self.letter_types):
                print str(index+1).rjust(2) + ". " + type
            prompt = "Select a letter to generate (or 0 if done selecting)."
            choices = str(range(len(self.letter_types)+1))
            self.to_gen.append(menu_choice(prompt, choices))
            if self.to_gen[-1] is 0:
                self.to_gen.pop()
                for i in range(len(self.to_gen)): # set to actual indexes
                    self.to_gen[i] = self.to_gen[i] - 1 # for value!
                break
        print self.to_gen
        # Now our to_gen indexes match those in letter_types.
        # TODO continue from here
