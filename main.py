import os
import re
import smtplib
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# ------------------------ GLOBAL VARIABLES -----------------#
MY_EMAIL = os.environ['MY_EMAIL']
PASSWORD = os.environ['PASSWORD']
ITEM_URL = "https://www.amazon.com/Graphics-Drawing-Function-Battery-Free-Pressure/dp/B07BGZ81N3/ref=sr_1_1_sspa?crid=3NFPIWC88MM8Q&keywords=huion+kamvas+pro+13+gt-133+graphics+drawing+monitor&qid=1647145208&sprefix=HUION+KAMVAS+Pro+13+GT-133%2Caps%2C143&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyM0NUUFdPWENEMk5SJmVuY3J5cHRlZElkPUEwODgzMDkzMUM2TTFUOFpFWlNWTyZlbmNyeXB0ZWRBZElkPUEwMjczMjI3MTNTQkJWOVE1U0VDRiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="
BROWSER_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Get the html for the webpage
response = requests.get(url=ITEM_URL, headers=BROWSER_HEADER)

# make the soup
soup = BeautifulSoup(response.text, "lxml")
# grab the element and parse it to get the right data
selection = str(soup.find_all(class_="a-offscreen")[0])
price = float(re.split('>', selection)[1].split('<')[0].split('$')[1])

# check to compare the price then send email if it meets the condition
if price < 250:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=os.environ['RECEIVE_EMAIL'],
            msg="Subject:AMAZON PRICE TRACKER ALERT!\n\n"
                "Product: HUION KAMVAS Pro 13 GT-133 Graphics Drawing Monitor\n"
                f"Current Price: {price}\n"
                f"Buy Here: {ITEM_URL}")
