#!/usr/bin/env python3
# lib/debug.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Base, User, Review, Destination, Booking, TourGuide
from datetime import datetime

destinations=session.query(Destination).all()

for destination in destinations:
       print(f"{destination.id}, {destination.name}, Ksh {destination.price}, {destination.duration} days, {destination.location}, {destination.description}")
