from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from lib.model import Base, User, Review, Destination, Booking, TourGuide
from datetime import datetime

date_str = '06-07-2025'

date_obj = datetime.strptime(date_str, '%d-%m-%Y').date()

# Create database engine and session
engine = create_engine('sqlite:///lib/tours.db')
Base.metadata.create_all(engine)

Session= sessionmaker(bind=engine)
session = Session()

# Users
users = [
    User(name="Makeda Mwolovi", email="makkmwolovi@gmail.com"),
    User(name="Brian Omog", email="brianomog@gmail.com")
]
session.add_all(users)
session.commit()

# Destinations
destinations = [
    Destination(
        name="Mount Kenya",
        price=28000,
        duration=3,
        location="Central Kenya",
        description="Experience the breathtaking beauty of Mount Kenya with guided hikes, wildlife spotting, and stunning alpine views."
    ),
    Destination(
        name="Watamu",
        price=65000,
        duration=2,
        location="Coast",
        description="Relax in the white sandy beaches of Watamu, enjoy snorkeling in marine parks, and explore coastal Swahili culture."
    ),
    Destination(
        name="Kakamega Forest",
        price=15000,
        duration=2,
        location="Western Kenya",
        description="Visit Kenya’s only tropical rainforest to see rare birds, butterflies, and ancient trees in a serene environment."
    ),
    Destination(
        name="Amboseli",
        price=47000,
        duration=3,
        location="Southern Kenya",
        description="Explore Amboseli National Park with its iconic views of Mount Kilimanjaro and herds of elephants roaming the plains."
    ),
    Destination(
        name="Maasai Mara",
        price=42000,
        duration=4,
        location="Southwestern Kenya",
        description="Witness the Great Migration, interact with Maasai culture, and go on thrilling game drives in the world-famous Mara."
    ),
    Destination(
        name="Diani",
        price=50000,
        duration=3,
        location="South Coast",
        description="Enjoy luxury beach resorts, vibrant nightlife, and water sports in the tropical paradise of Diani."
    ),
    Destination(
        name="Jinja",
        price=60000,
        duration=2,
        location="Eastern Uganda",
        description="Adventure capital of East Africa with white-water rafting, bungee jumping, and the source of the Nile."
    ),
    Destination(
        name="Kabaale Lake Bunyonyi",
        price=70000,
        duration=3,
        location="Western Uganda",
        description="Discover crater lakes, rolling hills, and traditional Ugandan hospitality in the scenic Kabaale region."
    )
]
session.add_all(destinations)
session.commit()

# Tour Guides (destination_id refers to the actual destinations above)
guides = [
    TourGuide(
        name="Kenneth Mugume",
        experience="3 years",
        languages='Luganda',
        fee=15000,
        rating=5,
        destination_id=7
    ),
    TourGuide(
        name="Robert Tumusiime",
        experience="4 years",
        fee=12000,
        languages= 'Tooro',
        rating=4.6,
        destination_id=8
    ),
    TourGuide(
        name="James Kimani",
        experience="5 years",
        fee=10000,
        languages= 'Kikuyu',
        rating=4.7,
        destination_id=1
    ),
    TourGuide(
        name="Aisha Mohammed",
        experience="3 years",
        fee=10000,
        languages='Kiswahili',
        rating=4.5,
        destination_id=2
    ),
    TourGuide(
        name="Peter Oloitok",
        experience="4 years",
        fee=15000,
        languages= 'Maasai',
        rating=4.6,
        destination_id=5
    ),
    TourGuide(
        name="Jacob Ojiambo",
        experience="2 years",
        fee=5000,
        languages= 'Luhya',
        rating=4,
        destination_id=3
    ),
    TourGuide(
        name="James Mukasa",
        experience="2 years",
        fee=8000,
        languages='Luganda',
        rating=4,
        destination_id=7
    )
]
session.add_all(guides)
session.commit()

# Bookings 
bookings = [
    Booking(
        user_id=1,
        name="Makeda",
        email="makkmwolovi@gmail.com",
        destination_id=4,
        date=date_obj,
        people=2,
        price=72000
    )
]
session.add_all(bookings)
session.commit()

#  Reviews (referencing existing booking_id and destination_id)
reviews = [
    Review(
        destination_id=6,
        booking_id=1,
        name="Mercy",
        comment="Nice and clean beaches",
        rating=5
    ),
    Review(
        destination_id=2,
        booking_id=1,
        name="Juliet",
        comment="Loved the marine park!",
        rating=4
    ),
    Review(
        destination_id=4,
        booking_id=1,
        name='',
        comment="Amazing wildlife and views.",
        rating=4
    )
]
session.add_all(reviews)
session.commit()

print("✅ Database seeded successfully!")
