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
    location_input = input("Enter the location you want to filter by: ").strip().lower()#strip removes extra white spaces
    
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

# helpers function fr creeating user

def get_or_create_user(session, name, email):
    user = session.query(User).filter_by(email=email).first()
    if user:
        # Update the user's name if it's missing or empty
        if not user.name or user.name.strip() == "":
            user.name = name.strip().title()
            session.commit()
        print(f"Welcome back, {user.name}!")
        return user
    else:
        # Create new user with name and email
        user = User(name=name.strip().title(), email=email.strip().lower())
        session.add(user)
        session.commit()
        print(f"Welcome, {user.name}!")
        return user



def book_destination(session):
    

    try:
        # Step 1: Select destination
        dest_id = input("Please enter the ID of the destination you would like to book: ").strip()
        destination = session.query(Destination).filter_by(id=int(dest_id)).first()
        if not destination:
            print("Destination not found.")
            return

        # Step 2: Identify user by email and name
        email = input("Please enter a valid email: ").strip().lower()
        name = input("Please enter your name: ").strip()

        # Step 3: Get or create user
        user = get_or_create_user(session, name, email)

        # Step 4: Ask for travel date
        date_str = input("Please input the date you would like to travel (DD-MM-YYYY): ").strip()
        try:
            travel_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")
            return

        # Step 5: Ask for number of people
        try:
            people = int(input("Please input the number of people travelling: ").strip())
            if people < 1:
                print("Number of people must be at least 1.")
                return
        except ValueError:
            print("Please enter a valid number of people.")
            return

        print("Note: Price shown on destination is per person.\n")

        # Step 6: Tour guide logic
        wants_guide = input("Would you like a tour guide for this trip? (yes/no): ").strip().lower()
        selected_guide = None

        if wants_guide == "yes":
            guides = session.query(TourGuide).filter_by(destination_id=destination.id).all()
            if guides:
                print("\nAvailable Tour Guides:")
                for guide in guides:
                    print(f"{guide.id}: {guide.name} - {guide.experience} years experience - Fee: Ksh {guide.fee}")
                try:
                    guide_id = int(input("Enter the ID of the tour guide you'd like to book: ").strip())
                    selected_guide = session.query(TourGuide).filter_by(id=guide_id, destination_id=destination.id).first()
                    if selected_guide:
                        print(f"\nAssigning tour guide: {selected_guide.name} - {selected_guide.experience} years experience - Fee: Ksh {selected_guide.fee}")
                    else:
                        print("Invalid tour guide selection. Proceeding without a guide.")
                except ValueError:
                    print("Invalid input. Proceeding without a guide.")
            else:
                print("Sorry, there are no tour guides available for this destination.")

        # Step 7: Calculate total cost
        base_cost = destination.price * people
        guide_fee = selected_guide.fee if selected_guide else 0
        total_price = base_cost + guide_fee

        # Step 8: Create booking record
        new_booking = Booking(
            user_id=user.id,
            destination_id=destination.id,
            email=email,
            date=travel_date,
            people=people,
            price=total_price,
            tour_guide_id=selected_guide.id if selected_guide else None
        )
        session.add(new_booking)
        session.commit()

        # Step 9: Confirm booking
        print(f"\n🎉 Booking confirmed for {destination.name} on {travel_date} for {people} people!")
        print(" Breakdown:")
        print(f" - Base cost (Ksh {destination.price} x {people}): Ksh {base_cost}")
        if selected_guide:
            print(f" - Tour guide fee ({selected_guide.name}): Ksh {guide_fee}")
        print(f" ✅ Total price: Ksh {total_price}")

    except Exception as e:
        session.rollback()
        print("❌ Booking failed:", e)

def view_user_bookings(session):
    email = input("Enter your email to view your bookings: ").strip().lower()

    # Use ilike for case-insensitive search
    user = session.query(User).filter(User._email.ilike(email)).first()

    if not user:
        print("No user found with that email.")
        # Debug: List all emails in DB to check what's stored
        print("Current emails in system:")
        for u in session.query(User).all():
            print(f" - {u.email}")
        return

    bookings = session.query(Booking).filter_by(user_id=user.id).all()
    if not bookings:
        print("You have no bookings yet.")
        return

    print(f"\nBookings for {user.name} ({user.email}):")

    for i, booking in enumerate(bookings, 1):
        destination = booking.destination
        guide = session.query(TourGuide).filter_by(id=booking.tour_guide_id).first() if booking.tour_guide_id else None

        print(f"\n{i}. Destination: {destination.location}")
        print(f"   Date: {booking.date}")
        print(f"   People: {booking.people}")
        if guide:
            print(f"   Tour Guide: {guide.name} ({guide.experience} yrs) — Ksh {guide.fee}")
        print(f"   Total Price: Ksh {booking.price}")

        #display all users booked
def show_all_users(session):
    print("\n Current Users in the System: ")

    for user in session.query(User).all():
        print(f"ID: {user.id} NAME: {user.name} EMALI:{user.email}")


from datetime import datetime

from datetime import datetime

def updating_a_booking(session):
    email = input("Please enter your email to see your current bookings: ").strip().lower()
    
    user = session.query(User).filter(User._email.ilike(email)).first()
    if not user:
        print("No user found with that email.")
        return
    
    bookings = session.query(Booking).filter_by(user_id=user.id).all()
    if not bookings:
        print("You have no bookings to update.")
        return
    
    print("\nYour bookings:")
    for idx, booking in enumerate(bookings, start=1):
        dest = booking.destination.name
        date = booking.date
        people = booking.people
        print(f"{idx}. Destination: {dest}, Date: {date}, People: {people}")
    
    try:
        choice = int(input("Select the number of the booking you want to update: "))
        if choice < 1 or choice > len(bookings):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    booking_to_update = bookings[choice - 1]
    
    # Update date
    new_date_str = input(f"Enter new travel date (DD-MM-YYYY) or press Enter to keep current ({booking_to_update.date}): ")
    if new_date_str.strip() != "":
        try:
            new_date = datetime.strptime(new_date_str, "%d-%m-%Y").date()
            booking_to_update.date = new_date
        except ValueError:
            print(" Invalid date format. Update cancelled.")
            return
    
    # Update number of people
    new_people_str = input(f"Enter new number of people or press Enter to keep current ({booking_to_update.people}): ")
    if new_people_str.strip() != "":
        try:
            new_people = int(new_people_str)
            if new_people < 1:
                print("Number of people must be at least 1.")
                return
            booking_to_update.people = new_people
        except ValueError:
            print(" Invalid number entered. Update cancelled.")
            return
    
    # Recalculate total price (tour guide fee stays the same)
    base_cost = booking_to_update.destination.price * booking_to_update.people
    guide_fee = 0
    if booking_to_update.tour_guide_id:
        guide = session.query(TourGuide).filter_by(id=booking_to_update.tour_guide_id).first()
        if guide:
            guide_fee = guide.fee
    total_price = base_cost + guide_fee
    booking_to_update.price = total_price
    
    try:
        session.commit()
        print("\n Booking updated successfully!")
        print(f"New Details:")
        print(f" - Destination: {booking_to_update.destination.location}")
        print(f" - Date: {booking_to_update.date}")
        print(f" - People: {booking_to_update.people}")
        if guide_fee:
            print(f" - Tour Guide fee: Ksh {guide_fee}")
        else:
            print(" - Tour Guide: None")
        print(f" - Total Price: Ksh {total_price}")
    except Exception as e:
        session.rollback()
        print(" Failed to update booking:", e)
        #deleting a booking
def delete_booking(session):
    email = input("Please enter your email to see your current bookings: ").strip().lower()

    # Find user by email
    user = session.query(User).filter(User._email.ilike(email)).first()
    if not user:
        print("No user found matching that email")
        return

    # Find bookings for that user
    bookings = session.query(Booking).filter_by(user_id=user.id).all()
    if not bookings:
        print("No bookings found for that user")
        return

    # Display bookings
    print("\nYour current bookings are:")
    for index, booking in enumerate(bookings, start=1):
        dest = booking.destination.name
        date = booking.date
        people = booking.people
        print(f"{index}, Destination: {dest} Date: {date} People: {people}")

    # User selects booking to delete
    choice = input("Select the number of booking you want to delete: ")

    try:
        choice = int(choice)
        if choice < 1 or choice > len(bookings):
            print("Invalid selection")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    booking_to_delete = bookings[choice - 1]  # zero-based index

    confirm = input(f"Are you sure you want to delete booking to {booking_to_delete.destination.name} on {booking_to_delete.date}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deleting the booking cancelled")
        return

    try:
        session.delete(booking_to_delete)
        session.commit()
        print("Booking was deleted successfully")
    except Exception as e:
        session.rollback()
        print("Failed to delete the booking:", e)
      



# Main menu for CLI
def main_menu():
    while True:
        print("\n--- TOUR BOOKING SYSTEM ---")
        print("1. View all destinations")
        print("2. Filter destinations by location")
        print("3. Make a new booking")
        print("4. View all users booked")
        print("5. View bookings")
        print("6. Update bookings")
        print("7. Delete bookings")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_and_choose_destination()
        elif choice == "2":
            filter_destinations_by_location()
        elif choice == "3":
            book_destination(session)
        elif choice =="4":
            show_all_users(session)
        elif choice == "5":
            view_user_bookings(session)
        elif choice == "6":
            updating_a_booking(session)
        elif choice == "7":
            delete_booking(session)
        elif choice == "8":
            print(f"GoodBye")             
            break
        else:
            print("Invalid choice. Try again.")