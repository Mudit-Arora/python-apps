import pandas
from abc import ABC, abstractmethod # abc stands for abstract base class

df = pandas.read_csv("hotels.csv", dtype={"id": str})


# Abstract class: a class that cannot be instantiated directly. It is meant to
# be subclassed, and it can declare abstract methods that subclasses MUST
# implement. We create one by inheriting from `ABC` (Abstract Base Class).
class Bookable(ABC):
    # Class variable: shared by ALL instances of the class (and its subclasses).
    # It belongs to the class itself, not to any single instance. Changing it
    # via the class affects every instance that hasn't shadowed it.
    booking_fee = 5.0

    # Abstract method: declared with @abstractmethod. Subclasses are REQUIRED
    # to override this method, otherwise they also become abstract and cannot
    # be instantiated.
    @abstractmethod
    def book(self):
        """Subclasses must define how the booking is performed."""
        pass

    @abstractmethod
    def available(self):
        """Subclasses must define how availability is checked."""
        pass


class Hotel(Bookable):
    # Class variable: a counter shared across every Hotel instance. We use it
    # below in a class method to keep track of how many hotels have been
    # created in this run.
    instance_count = 0

    # Magic method (a.k.a. "dunder" method): __init__ is called automatically
    # when a new instance is created. Magic methods have names surrounded by
    # double underscores and let our class hook into Python's built-in
    # behavior (construction, printing, equality, length, etc.).
    def __init__(self, hotel_id):
        # Instance variables: attributes that belong to THIS specific object
        # (accessed via `self`). Each Hotel instance has its own copy of
        # `hotel_id` and `name`.
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

        # Modifying the class variable through the class itself so the change
        # is visible to all instances.
        Hotel.instance_count += 1

    # Magic method: __str__ defines what `str(hotel)` and `print(hotel)`
    # produce. Useful for friendly, human-readable output.
    def __str__(self):
        return f"Hotel({self.hotel_id}, {self.name})"

    # Magic method: __repr__ defines the "official" representation, typically
    # used when debugging or printing a list of objects.
    def __repr__(self):
        return f"Hotel(hotel_id={self.hotel_id!r})"

    # Magic method: __eq__ defines what `==` means for our class. Two hotels
    # are considered equal when they share the same id.
    def __eq__(self, other):
        if not isinstance(other, Hotel):
            return NotImplemented
        return self.hotel_id == other.hotel_id

    # Instance method: operates on a specific instance through `self`. It can
    # read/modify that instance's data. This is the most common kind of method.
    def book(self):
        """Book this hotel by setting its availability to 'no'."""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    # Instance method using the class variable defined on the abstract parent.
    def total_price(self, nights, price_per_night):
        return nights * price_per_night + Bookable.booking_fee

    # Property: lets us expose a method as if it were a simple attribute.
    # Callers write `hotel.available` (no parentheses) instead of
    # `hotel.available()`. Great for computed/read-only values.
    @property
    def available(self):
        """Return True if the hotel is currently available."""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return availability == "yes"

    # Class method: receives the class itself (`cls`) as the first argument
    # rather than an instance. It can read/modify class-level state and is
    # often used for alternative constructors or class-wide operations.
    @classmethod
    def get_instance_count(cls):
        """Return how many Hotel objects have been created so far."""
        return cls.instance_count

    # Static method: belongs to the class namespace but does NOT receive
    # `self` or `cls`. It behaves like a plain function; we put it on the
    # class because it's logically related to it.
    @staticmethod
    def is_valid_id(hotel_id):
        """Validate that a hotel id is a non-empty string of digits."""
        return isinstance(hotel_id, str) and hotel_id.isdigit()


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        # Instance variables tied to this particular ticket.
        self.customer_name = customer_name
        self.hotel = hotel_object

    # Instance method: builds the ticket text from the instance's data.
    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content
