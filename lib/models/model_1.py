from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    

    bookings = relationship('Booking', back_populates='user', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)  # User email if needed
    date = Column(Date)  # Use Date type for date columns
    people = Column(Integer)
    price = Column(Float)
    destination_id = Column(Integer, ForeignKey('destinations.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='bookings')
    destination = relationship('Destination', back_populates='bookings')


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Integer)
    comment = Column(String)  # Add a comment field for review text
    destination_id = Column(Integer, ForeignKey('destinations.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='reviews')
    destination = relationship('Destination', back_populates='reviews')

class GuideDestination(Base):
    __tablename__ = 'guide_destinations'  # use lowercase with underscores

    id = Column(Integer, primary_key=True, autoincrement=True)
    guide_id = Column(Integer, ForeignKey('tour_guides.id'))
    destination_id = Column(Integer, ForeignKey('destinations.id'))

    guide = relationship('TourGuide', back_populates='guide_destinations')
    destination = relationship('Destination')


class TourGuide(Base):
    __tablename__ = 'tour_guides'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    experience=Column(String)
    languages = Column(String)
    rating=Column(Integer)

    destinations = relationship('Destination', back_populates='tour_guide')
    guide_destinations = relationship('GuideDestination', back_populates='guide') #this guy references the attribute guide in the model above


class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    duration = Column(Integer)
    location = Column(String)
    description = Column(String)
    tour_guide_id = Column(Integer, ForeignKey('tour_guides.id'))

    bookings = relationship('Booking', back_populates='destination', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='destination', cascade='all, delete-orphan')
    tour_guide = relationship('TourGuide', back_populates='destinations')

    # Create engine and sessionmaker
engine = create_engine('sqlite:///lib/tours.db')
Session = sessionmaker(bind=engine)
session=Session()


