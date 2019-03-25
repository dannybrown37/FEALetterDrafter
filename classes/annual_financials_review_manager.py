import os
import datetime
import mailmerge # pip install docx-mailmerge
from functions.validate import (
    menu_choice,
    get_bool,
    get_bool_or_na,
    get_case_number,
    get_string
)


class AFReviewManager(object): # AnnualFinancials
    def __init__(self):
        # needed info for header // could attach to case_data_manager but meh
        self.review_results = {
            "review_date" : datetime.datetime.today().strftime('%B %d, %Y'),
            "case_number" : get_case_number(),
            "condo_name" : get_string("What is the condominium name?")
        }

        # determine proper reporting level
        self.reporting_level = self.get_annual_revenue()
        self.review_results["correct_level"] = self.check_reporting_level()

        # branch off appropriately based on reporting level
        if "Report of Cash Receipts and Disbursements" in self.reporting_level:
            self.report_component_review()
            self.generate_memo("Report")
        else:
            self.statement_component_review()
            self.generate_memo("Statement")

    def generate_memo(self, memo_type):
        self.make_bools_into_strings() # for printing bools into docx

        # file stuff
        if memo_type == "Report":
            template_name = (
                "document_review_templates/FinancialReportReview_Template.docx"
            )
        elif memo_type == "Statement":
            template_name = (
                "document_review_templates/FinancialStatementReview_template.docx"
            )
        script_dir = os.path.dirname("main.py")
        absolute_path = os.path.join(script_dir, template_name)

        # create the document itself now
        document = mailmerge.MailMerge(absolute_path)
        document.merge(**self.review_results)

        # output our merged document
        output_name = "%s %s Financial %s Review Notes.docx" % (
            self.review_results["case_number"],
            self.review_results["condo_name"],
            memo_type
        )
        output_path = os.path.join(script_dir, output_name)
        document.write(output_path)
        print "\nYour Financial %s Review Memo has been generated!" % memo_type

    def statement_component_review(self):

        # for docx merge value
        self.review_results["reporting_level"] = self.reporting_level

        # check for accountant preparation for appropriate levels
        if "Compiled" not in self.reporting_level:
            self.review_results["accountant_prep"] = get_bool(
                "Did an independent certified public accountant prepare the\n"
                "financial statement as required by F.A.R. 61B-22.006(1)?"
            )
        else:
            self.review_results["accountant_prep"] = "N/A"

        # FINANCIAL STATEMENT COMPONENTS
        prompt = (
            "\n\n"
            "Was each of the following components included in the financial\n"
            "statements pursuant to F.A.R. 61B-22.006(2)?"
        )
        print prompt

        if "Compiled" not in self.reporting_level:
            self.review_results["accountant_report"] = get_bool(
                "Accountant's or auditor's report?"
            )
        else:
            self.review_results["accountant_report"] = "N/A"

        self.review_results["balance_sheet"] = get_bool("Balance sheet?")

        self.review_results["revenues_expenses"] = get_bool(
            "Statement of revenues and expenses?"
        )

        self.review_results["changes_funds"] = get_bool(
            "Statement of changes in fund balances?"
        )

        self.review_results["cash_flows"] = get_bool(
            "Statement of cash flows?"
        )

        self.review_results["notes"] = get_bool(
            "Notes to financial statements?"
        )

        # RESERVE DISCLOSURES
        prompt = (
            "\n\nWas each of the following reserve disclosures provided\n"
            "regardless of whether reserves have been waived for the fiscal\n"
            "period covered by the financial statements?"
        )
        print prompt

        self.review_results["beginning_reserves"] = get_bool(
            "The beginning balance in each reserve account as of the\n"
            "beginning of the fiscal period covered by the financial statement?"
        )

        self.review_results["reserve_additions"] = get_bool(
            "The amount of assessments and other additions to each reserve\n"
            "account including authorized transfers from other reserve accounts?"
        )

        self.review_results["reserve_expenditures"] = get_bool(
            "The amount expended or removed from each reserve account,\n"
            "including authorized transfers to other reserve accounts?"
        )

        self.review_results["ending_reserves"] = get_bool(
            "The ending balance in each reserve account as of the end of the\n"
            "fiscal period covered by the financial statement?"
        )

        self.review_results["annual_funding"] = get_bool(
            "The amount of annual funding required to fully fund each reserve\n"
            "account, or pool of accounts, over the remaining useful life of\n"
            "the applicable asset or group of assets?"
        )

        self.review_results["reserves_manner"] = get_bool(
            "The manner by whice reserve items were estimated, the date the\n"
            "estimates were last made, the association's policies for allocating\n"
            "reserve fund interest, and whether reserves have been waived during\n"
            "the period covered by the financial statements?"
        )

        rare_disclosures = get_bool(
            "Do rarely required disclosures apply? These include unit income\n"
            "and expense allocation, special assessments, limited common\n"
            "elements, and guarantees."
        )

        if rare_disclosures is False:
            self.review_results["method_allocation"] = "N/A"
            self.review_results["special_assessments"] = "N/A"
            self.review_results["limited_common_elements"] = "N/A"
            self.review_results["guarantee_disclosures"] = "N/A"
            return

        # rarely addressed disclosures requirements
        prompt = (
            "The following disclosure requirements may not be required.\n"
            "If not required, enter N/A. Statutory language follows:"
        )

        self.review_results["method_allocation"] = get_bool_or_na(
            "The method by which income and expenses were allocated to the\n"
            "unit owners."
        )

        self.review_results["special_assessments"] = get_bool_or_na(
            "The specific purpose or purposes of any special assessments\n"
            "to unit owners pursuant to Section 718.116(10), F.S., and the\n"
            "amount of each special assessment and the disposition of the\n"
            "funds collected."
        )

        self.review_results["limited_common_elements"] = get_bool_or_na(
            "The amount of revenues and expenses related to limited common\n"
            "elements shall be disclosed when the association maintains the\n"
            "limited commons elements and the expense is apportioned to those\n"
            "unit owners entitled to exclusive use of the limited common\n"
            "elements."
        )

        self.review_results["guarantee_disclosures"] = get_bool_or_na(
            "If a guarantee pursuant to Section 718.116(9), F.S., existed at\n"
            "any time during the fiscal year, the financial statements shall\n"
            "disclose the following:\n"
            "1. Period of time covered by the guarantee;\n"
            "2. The amount of common expenses incurred during the guarantee\n"
            "   period.\n"
            "3. The amount of assessments charged to non=developer unit\n"
            "   owners during the guarantee period.\n"
            "4-7 etc."
        )

    def report_component_review(self):
        # Checking for everything in FS 718.111(13)(b)2.
        self.review_results["receipts"] = get_bool(
            "Has the association disclosed \"the amount of receipts by accounts"
            "\nand receipt classifications\"?"
        )

        self.review_results["expenses"] = get_bool(
            "Has the association disclosed \"the amount of expenses by accounts"
            "\nand expense classifications\"?"
        )

        print "\nDid the association specifically include in its report:"

        self.review_results["security"] = get_bool("Security costs?")
        self.review_results["pro_and_man"] = get_bool(
            "Professional and managment fees and expenses?"
        )
        self.review_results["taxes"] = get_bool("Taxes?")
        self.review_results["rec_facilities"] = get_bool(
            "Recreational facilities?"
        )
        self.review_results["refuse_utilities"] = get_bool(
            "Expenses for refuse collection and utility services?"
        )
        self.review_results["lawn"] = get_bool("Expenses for lawn care?")
        self.review_results["buildings"] = get_bool(
            "Costs for building maintenance and repair?"
        )
        self.review_results["insurance"] = get_bool("Insurance costs?")
        self.review_results["admin_salaries"] = get_bool(
            "Administration and salary expenses?"
        )
        self.review_results["reserves"] = get_bool(
            "Reserves accumulated for capital expenditures, deferred\n"
            "maintenance, and any other category for which the association\n"
            "maintains reserves."
        )

    def check_reporting_level(self):
        prompt = (
            "Florida Statute 718.111(13)(a) states:\n"
            "\"An association ... shall prepare a complete set of financial\n"
            "statements ... The financial statements must be based on the\n"
            "association's total annual revenues, as follows:\"\n"
            "1. $500,000 and more   = Audited Financial Statement\n"
            "2. $300,000 - $500,000 = Reviewed Financial Statement\n"
            "3. $150,000 - $300,000 = Compiled Financial Statement\n"
            "4. Less than $150,000  = Report of Cash Receipts and Disbursements"
            "\n\n"
            "Based on revenue, the association should be preparing a:\n"
            "\n%s.\n\n"
            "Is the association reporting at the appropriate level (or higher)?"
        ) % self.reporting_level
        return get_bool(prompt)

    def get_annual_revenue(self):
        prompt = (
            "1. $500,000 and more\n"
            "2. $300,000 - $500,000\n"
            "3. $150,000 - $300,000\n"
            "4. Less than $150,000\n"
            "\n"
            "Select the range that includes the association's annual revenue."
        )
        choice = menu_choice(prompt, "1234")

        if choice == 1:
            return "Audited Financial Statement"
        elif choice == 2:
            return "Reviewed Financial Statement"
        elif choice == 3:
            return "Compiled Financial Statement"
        elif choice == 4:
            return "Report of Cash Receipts and Disbursements"

    def make_bools_into_strings(self):
        # Make the bools strings for printing
        for key, value in self.review_results.iteritems():
            if self.review_results[key] == True:
                self.review_results[key] = "Yes"
            elif self.review_results[key] == False:
                self.review_results[key] = "NO"
