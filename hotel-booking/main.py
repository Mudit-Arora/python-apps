from re import L
import re
import pandas as pd

df = pd.read_csv("hotels.csv", dtype = {"id": str}) # using id column as str instead of int

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

print(df)
id = input("Enter the id of the hotel: ")
hotel = Hotel(id) # create hotel instance with the id
if hotel.availability(): # check if that specific hotel is available
    hotel.book()
    name = input("Enter your name: ")
    # instance of the ReservationTicket class
    reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
    print(reservation_ticket.generate(customer_name=name, hotel_object=hotel))
else:
    print("Hotel not available")