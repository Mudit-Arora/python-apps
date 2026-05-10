from re import L
import re
import pandas as pd

df = pd.read_csv("hotels.csv", dtype = {"id": str}) # using id column as str instead of int
df_cards = pd.read_csv("cards.csv", dtype = str).to_dict(orient="records") # using all columns as strings and converting to dictionary
df_secure_cards = pd.read_csv("card_security.csv", dtype = {"number": str}) # using number column as string

class User:
    def view_hotels(self):
        pass

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == hotel_id, "name"].squeeze()

    def book(self):
        """Book the hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False) # adding index so python doesnt add another column index

    def availability(self):
        """Check if the hotel is available"""
        # squeeze to only get the value of the available column
        avail= df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if avail == "yes":
            return True
        else:
            return False

class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_object = hotel_object

    def generate(self, customer_name, hotel_object):
        content = f"""
        Thank you for your reservation!
        Here are your booking details:
        Name: {customer_name}
        Hotel: {hotel_object.name}
        Hotel ID: {hotel_object.hotel_id}
        """
        return content

# parent class
class CreditCard:
    def __init__(self, number, expiration, holder, cvc):
        self.number = number
        self.expiration = expiration
        self.holder = holder
        self.cvc = cvc

    def validate(self):
        card_data = {"number": self.number, "expiration": self.expiration, "holder": self.holder, "cvc": self.cvc}
        if card_data in df_cards:
            return True
        else:
            return False

# child class that inherits from the parent class (CreditCard class)
class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_secure_cards.loc[df_secure_cards["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
id = input("Enter the id of the hotel: ")
hotel = Hotel(id) # create hotel instance with the id
if hotel.availability(): # check if that specific hotel is available
    credit_card = SecureCreditCard(number="1234567890123456", expiration="12/26", holder="John Doe", cvc="123")
    if credit_card.validate():
        if credit_card.authenticate(given_password="mypass1"):
            hotel.book()
            name = input("Enter your name: ")
            # instance of the ReservationTicket class
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate(customer_name=name, hotel_object=hotel))
        else:
            print("Credit card not authenticated")
    else:
        print("Credit card not valid")
else:
    print("Hotel not available")