#  Tour Booking CLI App

This is a command-line based Tour Booking Application built with Python, SQLAlchemy, and Alembic. The app allows users to book tours, manage bookings, leave reviews, and explore destinations with the help of tour guides.

---

## 📁 Project Structure
├── lib/
│ ├── model.py # SQLAlchemy models (User, Booking, Destination, Review, TourGuide)
│ ├── tours.db # SQLite database
│ ├── seed.py # Script to populate the database with initial data
├── alembic/
│ ├── versions/ # Auto-generated migration files
│ ├── env.py # Alembic migration environment config
├── alembic.ini # Alembic config file
├── README.md # Project documentation
├── main.py # (Your CLI logic file — if applicable)
├── requirements.txt # Dependencies


---

## 🚀 Features

- Users can:
  - Register by providing name and email
  - Book a destination with optional tour guide
  - View, update, and cancel bookings
- Tour Guides:
  - Are assigned to destinations
  - Include attributes like experience, languages, and rating
- Reviews:
  - Can be left anonymously or with a name
  - Include a rating and a comment
- Admin features (optional):
  - View all users/bookings/reviews

---

## Technologies Used

- Python 3.12.2
- SQLite (via SQLAlchemy ORM)
- Alembic (for migrations)
- Pipenv (optional - for dependency management)

## Database Setup
Migrations: alembic upgrade head
Seed the Database:python lib/seed.py/python -m lib.seed

## Launch the CLI app:
python lib/run.py or python -m lib.run

## Models Overview
# USER

name, email

One-to-Many: Bookings

# BOOKING

name, email, date, people, price

Foreign Keys: user_id, destination_id, tour_guide_id

# Destination

name, location, price, duration, description

One-to-Many: Bookings, Reviews, TourGuides

# TourGuide

name, experience, fee, languages, rating

FK: destination_id

# Review

name (optional), rating, comment

FK: destination_id, booking_id


