import os
import django
from faker import Faker
import random
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')  # Adjust your settings module
django.setup()

from events.models import Event, Category, Participant  # Adjust app name if needed

def populate_db():
    fake = Faker()

    # Create Categories
    categories = []
    for _ in range(5):
        cat = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.paragraph(),
        )
        categories.append(cat)
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(20):
        event = Event.objects.create(
            name=fake.sentence(nb_words=4),
            description=fake.text(max_nb_chars=200),
            date=fake.date_time_between(start_date='-1y', end_date='+1y'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants and assign random events
    participants = []
    for _ in range(50):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        # Assign between 1 to 5 random events to participant
        participant.events.set(random.sample(events, k=random.randint(1, 5)))
        participants.append(participant)
    print(f"Created {len(participants)} participants with events assigned.")

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
