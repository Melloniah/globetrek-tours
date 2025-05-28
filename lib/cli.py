# lib/cli.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .model import Base, engine, session, User, Review, Destination, Booking, TourGuide
from datetime import datetime



from .helpers import (
    exit_program,
    helper_1
)

# A user can choose a destination based on the ID
def list_and_choose_destination():
    destinations = session.query(Destination).all()
    
    print("Available Destinations:")
    for dest in destinations:
        print(f"{dest.id}. {dest.name} — Ksh {dest.price}, {dest.duration} days, {dest.location}")
    
    while True:
        try:
            choice = int(input("Enter the number of the destination you want to choose: "))
            selected = next((d for d in destinations if d.id == choice), None)
            if selected:
                print(f"\nYou chose: {selected.name} in {selected.location}")
                return selected
            else:
                print("Invalid choice. Please enter a valid destination number.")
        except ValueError:
            print("Please enter a valid integer.")

# Filter destinations by location
def filter_destinations_by_location():
    location_input = input("Enter the location you want to filter by: ").strip().lower()
    
    filtered = session.query(Destination).filter(
        Destination._location.ilike(f"%{location_input}%") #ilike helps in case insensitve searches
    ).all()
    
    if filtered:
        print(f"Destinations matching '{location_input}':")
        for dest in filtered:
            print(f"{dest.id}. {dest.name} — Ksh {dest.price}, {dest.duration} days, {dest.location}")
    else:
        print(f"No destinations found for location matching '{location_input}'.")

    return filtered

# Main menu for CLI
def main_menu():
    while True:
        print("\n--- TOUR BOOKING SYSTEM ---")
        print("1. View all destinations")
        print("2. Filter destinations by location")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_and_choose_destination()
        elif choice == "2":
            filter_destinations_by_location()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")