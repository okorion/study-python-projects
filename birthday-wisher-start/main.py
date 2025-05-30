import smtplib
import datetime as dt
import random

MY_EMAIL = "<EMAIL>"
MY_PASSWORD = "<PASSWORD>"

now = dt.datetime.now()
weekday = now.weekday()
if weekday == 1:
    with open("quotes.txt") as quotes_file:
        all_quotes = quotes_file.readlines()
        quote = random.choice(all_quotes)

        print(quote)
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="<RECEIVER_EMAIL>",
                msg=f"Subject:Monday Motivation\n\n{quote}"
            )
