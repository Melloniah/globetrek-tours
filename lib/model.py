from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column("name", String, nullable=False)
    _email = Column("email", String, unique=True, nullable=False)
    

    bookings = relationship('Booking', back_populates='user')
    @property
    def name(self):
        return self._name

    @name.setter    
    def name (self, value):
        if not isinstance (value, str):
            raise ValueError("Name must be a text and not a number.")
        self._name=value    


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value or not value.endswith('.com'):
            raise ValueError("Email must be a valid string and contain '@', and end with '.com'")
        self._email=value 


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    _email = Column("email", String)  # User email if needed
    date = Column(Date)  # Use Date type for date columns
    people = Column(Integer)
    _price = Column("price", Float)

    tour_guide_id = Column(Integer, ForeignKey('tour_guides.id'), nullable=True)
    destination_id = Column(Integer, ForeignKey('destinations.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates='bookings')
    destination = relationship('Destination', back_populates='bookings')
    tour_guide = relationship("TourGuide", back_populates="bookings")

    reviews=relationship('Review', back_populates='booking', cascade='all, delete-orphan') 
    #review and booking is one to many. A user can leave several reviews on one booking

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number.")
        self._price = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value or not value.endswith('.com'):
            raise ValueError("Email must be a valid string and contain '@', and end with '.com'")
        self._email=value        


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)
    _comment = Column("comment", String, nullable=False)  # Add a comment field for review text
    

    destination_id = Column(Integer, ForeignKey('destinations.id'))
    booking_id= Column(Integer, ForeignKey('bookings.id')) #reviews for that destination. 

    booking = relationship('Booking', back_populates='reviews') #one booking several reviews
    destination = relationship('Destination', back_populates='reviews')

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment (self, value):
        if not isinstance (value, str) or len(value.strip()) <5:
            raise ValueError("Review must be a text and be at least 5 characters.")
        self._comment=value

class TourGuide(Base):
    __tablename__ = 'tour_guides'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    experience=Column(String)
    fee = Column(Integer)
    languages = Column(String)
    rating=Column(Integer)

    destination_id=Column(Integer, ForeignKey('destinations.id'))
    
    #one destination many tourguides
    destination = relationship('Destination', back_populates='tour_guides')
    #several bookings one tour guide
    bookings = relationship("Booking", back_populates="tour_guide")
    

class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    _price = Column("price", Float)
    duration = Column(Integer)
    _location = Column("location", String)
    description = Column(String)


    bookings = relationship('Booking', back_populates='destination', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='destination', cascade='all, delete-orphan')
    #one to many:one destination can have many tourguides
    tour_guides= relationship('TourGuide', back_populates='destination', cascade='all, delete-orphan')

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number.")
        self._price = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not isinstance(value, str):
            raise ValueError("Location must be one of the destinations provided.")
        self._location= value


 


engine = create_engine("sqlite:///lib/tours.db")  
Session = sessionmaker(bind=engine)
session=Session()


