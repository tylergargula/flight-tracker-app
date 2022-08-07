from datetime import datetime, timedelta
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from user_manager import UserManager
import os

ORIGIN_CITY_IATA = "ORD"
DATE_TOMORROW = datetime.today() + timedelta(days=1)
DATE_6_MONTHS = datetime.today() + timedelta(days=180)

# Class definition
data_manager = DataManager()
sheet_data = data_manager.get_destination_date()
flight_search = FlightSearch()
notification = NotificationManager()
user_manager = UserManager()

# Sheety Credentials
first_name = os.environ["FIRST_NAME"]
last_name = os.environ["LAST_NAME"]
sheety_email = os.environ["SHEETY_EMAIL"]

user_manager.get_user_data(first_name, last_name, sheety_email)

if sheet_data[0]['iataCode'] == "":
    for row in sheet_data:
        row['iataCode'] = flight_search.get_destination_code(row["city"])
    # print(f"sheet_data:\n {sheet_data}")
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=DATE_TOMORROW,
        to_time=DATE_6_MONTHS
    )

    if flight is None:
        continue

    # Convert tuples to string
    int_flight_price = int(''.join(map(str, flight.price)))
    str_origin_airport = str(''.join(map(str, flight.origin_airport)))
    str_origin_city = str(''.join(map(str, flight.origin_city)))
    str_destination_airport = str(''.join(map(str, flight.destination_airport)))
    str_destination_city = str(''.join(map(str, flight.destination_city)))
    str_depart = str(''.join(map(str, flight.out_date)))
    str_return = str(''.join(map(str, flight.return_date)))

    # Link to Google flights using flight query params (subject to change)
    google_flight_link = f"https://www.google.com/travel/flights?q=Flights%20to%20{str_destination_airport}%20from%20{str_origin_airport}%20on%20{str_depart}%20through%20{str_return}"

    if int_flight_price < destination["lowestPrice"]:
        message = f'\nLow price alert!\nOnly ${int_flight_price} to fly from {str_origin_city}-{str_origin_airport} to {str_destination_city}-{str_destination_airport}, from {str_depart} to {str_return}.'

        if flight.stop_overs[0] > 0:
            message += f'\nFlight has {flight.stop_overs} stop over, via {flight.via_city}'
        try:
            notification.send_sms(message, google_flight_link)
        except AttributeError:
            pass
