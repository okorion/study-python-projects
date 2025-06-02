import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": token,
    "username": "hyounkyu",
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

response = requests.post(url=pixela_endpoint, json=user_params)
print(response.text)
