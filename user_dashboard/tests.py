from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
 
from .models import Event, Registration, Category, Feedback, User
from .views import *

class UserDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_user_dashboard_view(self):
        url = reverse('user_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_dashboard.html')

    def test_browse_events_view(self):
        url = reverse('browse_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_events.html')

    # Add more tests for other views as needed

# class EventModelTests(TestCase):
#     def test_event_creation(self):
#         event = Event.objects.create(title='Test Event', description='Test description', )
#         self.assertEqual(Event.objects.count(), 1)
#         self.assertEqual(event.title, 'Test Event')
    
#     # Add more tests for models, forms, etc. as needed

