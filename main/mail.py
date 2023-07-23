import smtplib
from email.message import EmailMessage

def send_mail(price,name):
    msg = EmailMessage()

    my_msg = f"""Dear customer, Your order has been placed please click the below link to proceed
    link to track your order
    order_id = 1vhdj56788
    www.track_order.com
    Thank you, ,{name}"""
    msg.set_content(my_msg)
    msg['Subject'] = 'iMediCare, Your order'

    msg['From'] = "pran19cs@cmrit.ac.in"
    msg['To'] = "rakr19cs@cmrit.ac.in"
    print(msg)

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("pran19cs@cmrit.ac.in", "qwerty@123")
    server.send_message(msg)
    server.quit()

send_mail(23,"ordered")