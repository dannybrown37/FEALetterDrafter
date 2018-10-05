import datetime
import uszipcode
import phonenumbers
from phonenumbers import PhoneNumberFormat
from phonenumbers import format_number
from nameparser import HumanName


def get_string(prompt):
    return raw_input("\n" + prompt + "\n> ")


def get_bool(prompt):
    q = raw_input("\n" + prompt + "\n> ").lower()
    acceptable = ['yes', '1', 'true', 'y', 'no', '0', 'false', 'n']
    while q not in acceptable or q is "":
        print "\nThat's not an acceptable response. Please try again. "
        q = raw_input(prompt + "\n> ")
    if q == "no" or q == "false" or q == "0" or q == "n":
        return False
    elif q == "yes" or q == "true" or q == "1" or q == "y":
        return True


def get_integer(prompt):
    num = raw_input("\n" + prompt + "\n> ")
    while not num.isdigit():
        print "\nYou must enter a number. Please try again. "
        num = raw_input("\n" + prompt + "\n> ")
    return int(num)


def get_case_number():
    case_number = raw_input("\nWhat is the case number?\n> ")
    while len(case_number) != 10 or case_number.isdigit() == False:
        case_number = raw_input("\nNope, try a valid case number.\n> ")
    return case_number


def get_certified_mail_number():
    response = get_string("Please enter the letter's certified mail number.")
    response = response.replace(" ", "")
    if response is "0":
        return "CERTIFIED_MAIL_NUMBER"
    while response.isdigit() == False or len(response) != 20:
        response = get_string("Nope, try a valid certified mail number.")
        response = response.replace(" ", "")
    return " ".join([response[i:i+4] for i in range(0, len(response), 4)])


def get_respondent_salutation(resp_contact):
    name = resp_contact.replace("Attn: ", "").replace("c/o ", "")
    name = HumanName(name)
    contact = name.title + " " + name.last
    q = get_bool("Is this the contact person's salutation? << %s >>" % contact)
    if q is False:
        contact = get_string("Enter respondent's salutation.")
    return contact


def get_due_date(letter_type):
    if letter_type == "ACKC" or letter_type == "CCCL_Need_Evidence":
        num_days = 8
    elif letter_type == "WL" or letter_type == "ALGL":
        num_days = 15
    else:
        num_days = get_integer("How many days until a response is due?")
    due = datetime.datetime.now()
    week_day = datetime.datetime.today().weekday()
    due += datetime.timedelta(days=num_days if week_day != 4 else num_days + 2)
    due = due.strftime("%B") + " " + str(due.day) + ", " + str(due.year)
    return due


def zip_find(recipient_type):
    code = get_string("Enter the " + recipient_type + "'s mailing zip code.")
    code = ''.join(char for char in code if char.isdigit())
    search = uszipcode.ZipcodeSearchEngine()
    myzip = search.by_zipcode(code)
    if not myzip:
        return get_string("Manually enter the city, state, and zip code.")
    else:
        return myzip.City + ", " + myzip.State + " " + code


def menu_choice(prompt, acceptable):
    response = raw_input("\n" + prompt + "\n> ")
    while response not in acceptable or response is "":
        print "\nThat's not an acceptable response. Please try again. "
        response = raw_input("\n" + prompt + "\n> ")
    if response.isdigit():
        return int(response)
    else:
        return response
