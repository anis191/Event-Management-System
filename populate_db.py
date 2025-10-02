import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')  # Replace with your project folder if needed
django.setup()

from events.models import Event, Category
from users.models import CustomUser

def populate_db():
    fake = Faker()

    # ---------------------------
    # Create Categories
    # ---------------------------
    categories = []
    for _ in range(5):
        cat = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.paragraph()
        )
        categories.append(cat)
    print(f"Created {len(categories)} categories.")

    # ---------------------------
    # Create Users
    # ---------------------------
    users = []
    for i in range(10):
        user = CustomUser.objects.create_user(
            username=fake.user_name() + str(i),  # usernames must be unique
            email=fake.email(),
            password="password123"  # default password for all fake users
        )
        users.append(user)
    print(f"Created {len(users)} users.")

    # ---------------------------
    # Create Events
    # ---------------------------
    events = []
    for _ in range(20):
        event = Event.objects.create(
            name=fake.sentence(nb_words=4),
            description=fake.paragraph(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories)
        )
        # Assign random users to event
        event.assign_to.set(random.sample(users, random.randint(1, 3)))
        # Optional: assign some RSVPs
        event.rsvp.set(random.sample(users, random.randint(0, 3)))
        events.append(event)

    print(f"Created {len(events)} events.")
    print("✅ Database populated successfully!")

if __name__ == "__main__":
    populate_db()
