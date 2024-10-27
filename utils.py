import smtplib
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = getenv("SENDER_APP_PASSWORD")
CHEF_EMAIL = getenv("CHEF_EMAIL")

def place_order(name, email, address, orders):
    total_price, orders_string = 0, "\n"
    for i, order in enumerate(orders):
        orders_string += f"{i + 1}. {order[4]}x {order[1]}\n"
        total_price += order[2]
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
    message = f"""Subject: Confirmation of your Order\n 

    Your order listed as below has been placed.
    {orders_string}
    Your Total is Rs. {total_price}, will be delivered at {address}
    """
    s.sendmail(SENDER_EMAIL, email, message)
    message = f"""Subject: New Order Placed\n

    Order includes the following items,
    {orders_string}
    Total price is Rs. {total_price}
    Address to be delivered is {address}"""
    s.sendmail(SENDER_EMAIL, CHEF_EMAIL, message)
    s.quit()
    return
