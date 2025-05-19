import requests
import smtplib
import os
from twilio.rest import Client

# This needs to be uploaded on pythonanywhere and set to execute(Schedule task) at morning 5 am
# (sl = 5.30 ahed of UTC + 5.30) Morning 5 am = 23.30 UTC (which is night 11.30pm + 5.30 = 5 am)
# Otherwise this will start the time when we run the code (Not from 5 am.)
# ################ change lat and long or time total checking hour if needed ###############


URL = "https://api.openweathermap.org/data/2.5/onecall"  # Endpoint
my_api_key = "Your Twillio API KEY"  # get form the twillio website


my_email = "Youremail@gmail.com"
my_password = "Password"   # this password get evjmuhullfguaohg from mail  generated
sender_email = "Sender email"

# most_frequent finder


def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


# #########total checking hour ####################
TOTAL_HOURS_NEED_TO_CHECK_FOR_RAIN = 18  # max 24
THIS_CODE_EXECUTION_START_TIME_MORNING = 5

# ############# LAT and long ###############
# house Kalmunai.
location = "Kalmunai"
house_longitude = "Your House longitude"
house_latitude = "Your House longitude"

# # university of Kelaniya
# university_longitude = 79.915840
# university_latitude = 6.972903


parameter = {
    "lat": house_latitude,
    "lon": house_longitude,
    "appid": angela_api_key,
    "exclude": "current,minutely,daily,alerts",
}

respond = requests.get(URL, params=parameter)
respond.raise_for_status()
weather_data = respond.json()

weather_slice = weather_data["hourly"][:TOTAL_HOURS_NEED_TO_CHECK_FOR_RAIN]

weather_conditions_list = []
will_rain = False
for hour_data in weather_slice:
    weather_id = hour_data["weather"][0]["id"]
    weather_description = hour_data["weather"][0]["description"]
    weather_conditions_list.append(weather_description)
    if weather_id < 700:  # If weather id less than 700 rain.
        will_rain = True

if will_rain:
    message_whatsapp = "☔☔☔☔It's going to rain today, Remember to Bring an umbrella.⛈🌦☔☔"
    message_mail = "It's going to rain today, Remember tp Bring an umbrella"
else:
    message_whatsapp = "No rain today, So No need for an umbrella.🌞☀🌤"
    # emoji works for WhatsApp.
    message_mail = "No rain today, So No need for an umbrella."
    # But for email error will come up.
    # so don't use emojis for email


detail_message_each_hour = ""
for each_hour in range(TOTAL_HOURS_NEED_TO_CHECK_FOR_RAIN):
    current_hour = THIS_CODE_EXECUTION_START_TIME_MORNING  # 5
    # su current hour start with 5 + 0 then increasing. (initial 5)
    current_hour += each_hour
    if current_hour > 12:
        evening_hour = current_hour - 12
        if evening_hour > 6:
            detail_message_each_hour += f"Night {evening_hour} - {weather_conditions_list[each_hour]}\n"
        else:
            detail_message_each_hour += f"Evening {evening_hour} - {weather_conditions_list[each_hour]}\n"
    else:
        detail_message_each_hour += f"Morning {current_hour} - {weather_conditions_list[each_hour]}\n"

# mail
with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=sender_email,
                        msg=f"Subject:Weather update in {location}\n\n{message_mail}\nToday Mostly {most_frequent(weather_conditions_list)}\n\n"
                            f"Hourly Weather Forecast\n{detail_message_each_hour}")


# whatsapp
Account_SID = "YOUR TWILLIO SID"  # like username
Auth_Token = "TOKEN"  # os.environ.get("AUTH_TOKEN")   # like password

client = Client(Account_SID, Auth_Token)

# Get this from your twillio account
from_whatsapp_number = "whatsapp:+14155123886"
# to_whatsapp_number = f"whatsapp:{os.environ.get('WHATSAPP')}"    # your number (notification receiver)
to_whatsapp_number = f"whatsapp:{+94771111193}"

client.messages.create(
    body=f"Subject:Weather update in {location}\n\n{message_whatsapp}\nToday Mostly {most_frequent(weather_conditions_list)}\n\n"
         f"Hourly Weather Forecast\n{detail_message_each_hour}",
    from_=from_whatsapp_number,
    to=to_whatsapp_number)


# command in pythonanywhere =  export WHATSAPP=+94779434493; python3 mw.py
