import smtplib

my_email = "ok.or.orion@gmail.com"
password = "<PASSWORD>"

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="",
        msg="Subject:Happy Birthday!\n\nHappy Birthday to you! Wishing you a wonderful day filled with joy and happiness!"
    )
