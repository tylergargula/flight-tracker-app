import requests
import os

SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_PRICES_ENDPOINT"]


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_date(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        sheety_result = response.json()
        self.destination_data = sheety_result["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            sheet_inputs = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=sheet_inputs
            )
            print(response.text)


