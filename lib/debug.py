#!/usr/bin/env python3
# lib/debug.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from lib.model import Base, engine, User, Review, Destination, Booking, TourGuide
from datetime import datetime

engine = create_engine("sqlite:///lib/tours.db")  
Session = sessionmaker(bind=engine)
session=Session()

destinations=session.query(Destination).all()

for destination in destinations:
       print(f"{destination.id}, {destination.name}, Ksh {destination.price}, {destination.duration} days, {destination.location}, {destination.description}")

users = session.query(User).all()
for user in users:
   print(f"{user.id}, {user.name}, {user.email}")


# Filter destinations by price
cheap = session.query(Destination).filter(Destination._price < 30000).all()
print(cheap)