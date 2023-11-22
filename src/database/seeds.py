from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import date

from models import Base, Contact
from db import URI


engine = create_engine(URI)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

fake = Faker('uk_UA')

# Create 30 fake contacts and insert them into the database
for _ in range(30):
    contact = Contact(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number(),
        birthday=fake.date_of_birth(minimum_age=21, maximum_age=50),
        additional=fake.text(max_nb_chars=20),  # Limit text to 20 characters
    )

    session.add(contact)

session.commit()