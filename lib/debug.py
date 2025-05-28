#!/usr/bin/env python3
# lib/debug.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .model import Base, engine, User, Review, Destination, Booking, TourGuide
from datetime import datetime

destinations=session.query(Destination).all()

for destination in destinations:
       print(f"{destination.id}, {destination.name}, Ksh {destination.price}, {destination.duration} days, {destination.location}, {destination.description}")

users = session.query(User).all()
for user in users:
   print(f"{user.id}, {user.name}, {user.email}")

# Get bookings for a specific user
user = session.query(User).filter_by(name="Makeda").first()
print(user.bookings)

# Filter destinations by price
cheap = session.query(Destination).filter(Destination.price < 30000).all()
print(cheap)