from django.test import TestCase, Client
from django.urls import reverse
import json

class SentimentAnalysisAPITest(TestCase):
    """Test case for the sentiment analysis API."""
    
    def setUp(self):
        """Set up the test client and sample data for the tests."""
        self.client = Client()
        self.url = reverse('sentiment_analysis')
        self.pos_data = {'sentence': 'Well done that was amazing'}
        self.neg_data = {'sentence': 'That was a terrible event, the food was not great'}
        self.invalid_data = {'sentence': ''}

    def test_sentiment_analysis_api_with_pos_valid_data(self):
        """Test the API with a valid positive sentence."""
        response = self.client.post(self.url, json.dumps(self.pos_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sentiment', response.json())
        self.assertIn(response.json()['sentiment'], ['positive'])

    def test_sentiment_analysis_api_with_neg_valid_data(self):
        """Test the API with a valid negative sentence."""
        response = self.client.post(self.url, json.dumps(self.neg_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sentiment', response.json())
        self.assertIn(response.json()['sentiment'], ['negative'])

    def test_sentiment_analysis_api_with_invalid_data(self):
        """Test the API with an invalid (empty) sentence."""
        response = self.client.post(self.url, json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
