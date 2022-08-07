import requests
import os

SHEETY_USER_ENDPOINT = os.environ["SHEETY_ENDPOINT"]


class UserManager:
    def __init__(self):
        self.user_data = {}

    def get_user_data(self, first_name, last_name, email):
        sheet_inputs = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }

        requests.post(
            url=SHEETY_USER_ENDPOINT,
            json=sheet_inputs,
        )

