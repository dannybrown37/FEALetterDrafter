
import os
import datetime
import mailmerge # pip install docx-mailmerge
from functions.validate import (
    get_case_number,
    get_string,
    get_bool,
    get_bool_or_na,
    get_bool_or_na_or_unknown,
    menu_choice
)

class BudgetReviewManager(object):
    def __init__(self):
        self.review_results = {
            "review_date" : datetime.datetime.today().strftime('%B %d, %Y'),
            "case_number" : get_case_number(),
            "condo_name" : get_string("What is the condominium name?")
        }

        self.rule_elements()
        self.step_through_statute()
        self.reserve_questions()
        self.notice_questions()
        self.generate_memo()

    def generate_memo(self):
        self.make_bools_into_strings() # for printing bools into docx

        # file stuff
        template_name = (
            "document_review_templates/BudgetReview_Template.docx"
        )
        script_dir = os.path.dirname("main.py")
        absolute_path = os.path.join(script_dir, template_name)

        # create the document itself now
        document = mailmerge.MailMerge(absolute_path)
        document.merge(**self.review_results)

        # output our merged document
        output_name = "%s %s Budget Review Notes.docx" % (
            self.review_results["case_number"],
            self.review_results["condo_name"]
        )
        output_path = os.path.join(script_dir, output_name)
        document.write(output_path)
        print "\nYour Budget Review Memo has been generated!"

    def rule_elements(self):
        self.review_results["common_expenses"] = get_bool(
            "The association is required to include the following elements\n"
            "in its annual budget. Indicate whether each was included:\n\n"
            "(a) State the estimated common expenses or expenditures on at\n"
            "    least an annual basis."
        )

        self.review_results["beg_end"] = get_bool(
            "(b) Disclose the beginning and ending dates of the period\n"
            "    covered by the budget."
        )

        self.review_results["unit_types_ass"] = get_bool(
            "(c) Show the total assessment for each unit type according to\n"
            "    the proportion of ownership on a monthly basis, or for any\n"
            "    other period for which assessments will be due."
        )

        self.review_results["reserves_full"] = get_bool(
            "(d) Reserves for capital expenditures and deferred maintenance\n"
            "    must be included in proposed annual budget and shall not be\n"
            "    waived or reduced prior to mailing proposed budget."
        )

        pool_or_straight = menu_choice(
            "Select the method of reserves accounting:\n"
            "1. Straight-line\n"
            "2. Pooled",
            "12"
        )

        if pool_or_straight is 1: #straight-line
            self.review_results["straight_line"] = True
            self.review_results["total_estimate"] = get_bool(
                "Does the association's reserve schedule include the following\n"
                "information for each asset for which reserves are maintained?"
                "\n\n1. The total estimated useful life of the asset."
            )
            self.review_results["remaining_estimate"] = get_bool(
                "2. The estimated remaining life of the asset."
            )
            self.review_results["replacement_cost"] = get_bool(
                "3. The estimated replacement cost or deferred maintenance\n"
                "   expense of the asset."
            )
            self.review_results["beginning_balance"] = get_bool(
                "4. The estimated fund balance as of the beginning of the\n"
                "    period for which the budget will be in effect."
            )
            self.review_results["dev_obligation"] = get_bool_or_na(
                "5. The developer's total funding obligation, when all units\n"
                "    are sold, for each converter reserve, if applicable.\n"
                "Enter \"N/A\" if this does not apply."
            )
            # empty strings for the other method of reserves
            self.review_results["pooled"] = ""
            self.review_results["pooled_total"] = ""
            self.review_results["pooled_remaining"] = ""
            self.review_results["pooled_replacement"] = ""
            self.review_results["pooled_balance"] = ""
        elif pool_or_straight is 2: #pooled
            self.review_results["pooled"] = True
            self.review_results["pooled_total"] = get_bool(
                "Does the association's pooled reserve schedule include the\n"
                "following information?\n\n"
                "1. The total estimated useful life of each asset within the\n"
                "   pooled analysis."
            )
            self.review_results["pooled_remaining"] = get_bool(
                "2. The estimated remaining useful life of each asset within\n"
                "   the pooled analysis."
            )
            self.review_results["pooled_replacement"] = get_bool(
                "3. The estimated replacement cost or deferred maintenance\n"
                "   expense of each asset within the pooled analysis."
            )
            self.review_results["pooled_balance"] = get_bool(
                "4. The estimated fund balance of the pooled reserve account\n"
                "   as of the beginning of the period for which the budget\n"
                "   will be in effect."
            )
            # emptry strings for the other methord of reserves
            self.review_results["straight_line"] = ""
            self.review_results["total_estimate"] = ""
            self.review_results["remaining_estimate"] = ""
            self.review_results["replacement_cost"] = ""
            self.review_results["beginning_balance"] = ""
            self.review_results["dev_obligation"] = ""

        self.review_results["other_reserves"] = get_bool_or_na(
            "Did the association include a separate schedule of any other\n"
            "reserve funds to be restricted by the association as a separate\n"
            "line item with the following minimum disclosures:\n"
            "1. The intended use of the restricted funds.\n"
            "2. The estimated fund balance of the item at the beginning of\n"
            "   period for which the budget will be in effect.\n"
            "Enter \"N/A\" if there is not evidence of other reserves."
        )



    def notice_questions(self):
        do_it = get_bool(
            "Is the 14-day noticing of the budget meeting under investigation?"
        )
        if do_it is False:
            self.review_results["notice_14"] = "N/A"
            self.review_results["notice_affidavit"] = "N/A"
        else:
            self.review_results["notice_14"] = get_bool_or_na_or_unknown(
                "Did the association notice the budget meeting at least 14\n"
                "days in advance? Hand delivery, mail, and electronic delivery\n"
                "are acceptable forms of notice.\n"
                "(Enter \"unknown\" if evidence is not yet obtained.)"
            )
            self.review_results["notice_affidavit"] = get_bool_or_na_or_unknown(
                "Did an officer or manager execute an affidavit attesting to\n"
                "the delivery of the 14-day budget meeting notice?\n"
                "(Enter \"unknown\" if evidence is not yet obtained.)"
            )

    def reserve_questions(self):
        self.review_results["reserves_waived"] = get_bool_or_na_or_unknown(
            "Have unit owners waived reserves with a majority vote at a duly\n"
            "called meeting?\n\n"
            "Enter \"N/A\" if reserve waivers not being investigated.\n"
            "Enter \"Unknown\" if evidence doesn't demonstrate either way\n"
            "AND if this is an allegation or issue under investigation."
        )

        if self.review_results["reserves_waived"] in [True, "N/A"]:
            self.review_results["reserve_accounts"] = "N/A"
            self.review_results["reserve_formula"] = "N/A"
        else:
            self.review_results["reserve_accounts"] = get_bool(
                "Does the budget include reserves for painting, paving,\n"
                "roofing, and any other item estimated at more than $10k?"
            )
            self.review_results["reserve_formula"] = get_bool(
                "Was amount to be reserved computed using a formula based on\n"
                "the estimated remaining useful life and estimated replacement\n"
                "cost or deferred maintenance expense of each reserve item."
            )


    # FS 718.112(2)(f)
    def step_through_statute(self):
        # detailed and classified
        self.review_results["classification"] = get_bool(
            "The proposed annual budget of estimated revenues and expenses\n"
            "must be detailed and must show the amounts budgeted by accounts\n"
            "and expense classifications...\n"
            "Does the budget meet this standard?"
        )

        # specific categories from FS 718.504(21), intro and first one
        self.review_results["assessments"] = get_bool(
            "The budget shall include, at a minimum, any applicable expenses\n"
            "listed in s. 718.504(21).\n\n"
            "Does the budget include the following expenses?\n\n"
            "(a) The estimated monthly and annual expenses of the condominium\n"
            "    and the association that are collected from unit owners by\n"
            "    assessments."
        )

        self.review_results["special_pay"] = get_bool_or_na(
            "(b) The estimated monthly and annual [amount owed] by the unit\n"
            "    owner to persons or entities other than the association, as\n"
            "    well as to the association, including fees assessed pursuant\n"
            "    to s. 718.113(1) for maintenance of limited common elements\n"
            "    where such costs are shared only by those entiteled to use\n"
            "    the limited common element, and the total estimated monthly\n"
            "    and annual expense. (Numerous exceptions listed.)\n\n"
            "Enter N/A if there is no evidence this expense applies."
        )

        # the list under subsection (c) starts here
        self.review_results["admin"] = get_bool(
            "Subsection (c) requires the following items specifically.\n"
            "Indicate whether they were included or if association marked\n"
            "these items as \"N/A\".\n\n"
            "Administration of the association?"
        )
        self.review_results["management"] = get_bool("Management fees?")
        self.review_results["maintenance"] = get_bool("Maintenance?")
        self.review_results["rec_rent"] = get_bool(
            "Rent for recreataional and other commonly used facilities?"
        )
        self.review_results["taxes_prop"] = get_bool(
            "Taxes upon association property?"
        )
        self.review_results["taxes_leased"] = get_bool(
            "Taxes upon leased areas?"
        )
        self.review_results["insurance"] = get_bool("Insurance?")
        self.review_results["security"] = get_bool("Security provisions?")
        self.review_results["other"] = get_bool("Other expenses?")
        self.review_results["operating"] = get_bool("Operating capital?")
        self.review_results["reserves"] = get_bool("Reserves?")
        self.review_results["division_fees"] = get_bool(
            "Fees payable to the division?"
        )
        self.review_results["unit_rent"] = get_bool(
            "Rent for the unit, if subject to a lease."
        )
        self.review_results["other_rent"] = get_bool(
            "Rent payable by the unit owner directly to the lessor or agent\n"
            "under any recreational lease or lease for the use of commonly\n"
            "used facilities, which use and payment is a mandatory condition\n"
            "of ownership and is not included in the common expense or\n"
            "assessments for common maintenance paid by the unit owners to\n"
            "the association."
        )

        self.review_results["min_months"] = get_bool(
            "(f) The estimated budget covers a period of at least 12 months."
        )

    def make_bools_into_strings(self):
        # Make the bools strings for printing
        for key, value in self.review_results.iteritems():
            if self.review_results[key] == True:
                self.review_results[key] = "Yes"
            elif self.review_results[key] == False:
                self.review_results[key] = "NO"
