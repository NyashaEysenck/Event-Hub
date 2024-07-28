# events/management/commands/load_random_events.py

from django.core.management.base import BaseCommand
from ...models import Event
from django.contrib.auth import get_user_model
from faker import Faker
import random
from datetime import timedelta

fake = Faker()
User = get_user_model()

def generate_random_events(num_events):
    events = []
    users = list(User.objects.all())  # Fetch all users to assign as creators
    for _ in range(num_events):
        title = fake.catch_phrase()
        description = fake.paragraph()
        location = fake.address()
        start_datetime = fake.date_time_between(start_date='+1d', end_date='+30d')
        end_datetime = start_datetime + timedelta(hours=random.randint(1, 6))
        created_by = random.choice(users)  # Assign a random user as the creator
        event = Event(
            title=title,
            description=description,
            location=location,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            created_by=created_by
        )
        events.append(event)
    return events

class Command(BaseCommand):
    help = 'Generate and load random events into the database'

    def handle(self, *args, **kwargs):
        num_events = 20  # Number of random events to generate
        random_events = generate_random_events(num_events)
        Event.objects.bulk_create(random_events)
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {num_events} random events'))
