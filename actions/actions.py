# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset
# import library
import math
import random
import re
# Make a regular expression
# for validating an Email
import smtplib

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


# Define a function for
# for validating an Email


def send(otp, email):
    # create smtp session
    sender_email = "sanksub29@gmail.com"
    sender_email_password = "29thApril2000"
    s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
    # start TLS for E-mail security
    s.starttls()
    # Log in to your gmail account
    s.login(sender_email, sender_email_password)

    message = "This for the verification purpose. Your OTP code is " + otp
    s.sendmail(sender_email, email, message)

    # close smtp session
    s.quit()


def check(email):
    # pass the regular expression
    # and the string in search() method
    if (re.search(regex, email)):
        return True

    else:
        return False


# function to generate OTP
def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be chaged
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def interest_rates(a):
    year_rates = {2005: [8, 5],
                  2007: [7.5, 1],
                  2008: [6, 2],
                  2009: [8, 6],
                  2010: [7, 4],
                  2011: [6, 2],
                  2012: [8.5, 5],
                  2013: [9, 7],
                  2014: [7, 3],
                  2015: [9, 6],
                  2016: [10, 8],
                  2017: [6, 2],
                  2018: [5, 6],
                  }

    if a >= 2007 and a <= 2018:

        value_list = year_rates[a]

        message = "The Interest rate was " + str(value_list[0]) + " % for " + str(value_list[1]) + " years "

    else:
        message = "The Interest rate was " + "4" + " % for " + "1" + " years "

    return message



class ValidateLoginForm(FormValidationAction):

    def name(self) -> Text:

        return "validate_login_form"

    def validate_emailid(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:

        global var
        var = generateOTP()
        """Validate cuisine value."""
        slot = tracker.get_slot("emailid")

        if (check(str(slot)) == True):
            send(var, slot)
            print("OTP SENT")
            print(var)
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"emailid": slot_value}

        else:
            dispatcher.utter_message(text="invalid email")
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"emailid": None}

    def validate_otp(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if str(slot_value) == var:

            # validation succeeded, set the value of the "cuisine" slot to value
            return {"otp": slot_value}


        else:
            dispatcher.utter_message(text="Invalid OTP ")
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"otp": None}


class ValidateYearForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_year_form"

    def validate_year(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[str, Any]:
        interest_year = tracker.get_slot("year")
        year_value = interest_rates(int(interest_year))
        dispatcher.utter_message(text=year_value)
        return {"year": slot_value}


class ActionResetAllSlots(Action):

    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
