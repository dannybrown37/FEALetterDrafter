import os
import mailmerge # pip install docx-mailmerge
from functions.validate import get_bool

class ConsentOrderManager(object):
    def __init__(self, dbm, cdm):
        self.dbm = dbm
        self.cdm = cdm
        self.get_merge_fields()
        self.generate_order()

    def get_merge_fields(self):
        # TODO when necessary, handle other orders
        self.file_name = (
            "admin_action_templates/ConsentOrderDeveloper_Template.docx"
        )

        # First get the merge fields that are in the consent order
        with mailmerge.MailMerge(self.file_name) as document:
            self.merge_fields = sorted(list(document.get_merge_fields()))

        # Then get the data for those fields
        self.merge_dict = {}
        for mf in self.merge_fields:
            if mf == "Respondent":
                self.merge_dict[mf] = self.cdm.case_list[1]
            elif mf == "Association":
                q = get_bool("Is association the respondent?")
                if not q:
                    self.merge_dict[mf] = raw_input(
                        "What is the {}? ".format(mf)
                    )
                else:
                    self.merge_dict[mf] = self.cdm.case_list[1]
            elif mf == "CaseNumber":
                self.merge_dict[mf] = str(self.cdm.case_list[0])
            elif mf == "Condominium":
                self.merge_dict[mf] = self.cdm.case_list[2]
            else:
                self.merge_dict[mf] = raw_input("What is the {}? ".format(mf))

    def generate_order(self):
        script_dir = os.path.dirname("main.py")
        absolute_path = os.path.join(script_dir, self.file_name)
        document = mailmerge.MailMerge(absolute_path)
        document.merge(**self.merge_dict)
        output_path = os.path.join(
            script_dir,
            "{} Consent Order.docx".format(self.cdm.case_list[0])
        )
        document.write(output_path)
        print "\nYour administrative action has been generated!"
