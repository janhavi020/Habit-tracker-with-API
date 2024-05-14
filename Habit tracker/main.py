import requests
from _datetime import datetime
import os

GENDER = "female"
WEIGHT_KG = 40
HEIGHT_CM = 160
AGE = 22

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("APP_KEY")


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()


sheet_endpoint = os.environ.get("SHEET_ENDPOINT")


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs,headers=headers)

    print(sheet_response.text)