import pandas as pd

df = pd.read_csv("hotels.csv")

class User:
    def view_hotels(self):
        pass

class Hotel:
    def __init__(self, hotel_id):
        pass

    def book(self):
        pass

    def availability(self):
        pass

class ReservationTicket:
    def generate(self, customer_name, hotel_object):
        pass

print(df)
id = input("Enter the id of the hotel: ")
hotel = Hotel(id) # unique id 
if hotel.availability(): # check if that specific hotel is available
    hotel.book()
    name = input("Enter your name: ")
    # instance of the ReservationTicket class
    reservation_ticket = ReservationTicket(name, hotel)
    print(reservation_ticket.generate())
else:
    print("Hotel not available")