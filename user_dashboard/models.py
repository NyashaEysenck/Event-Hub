from django.db import models
from django.contrib.auth import get_user_model
from superuser_dashboard.models import Event, Category
User = get_user_model()

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()
    feedback_datetime = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=10, default='positive', choices=[('positive', 'Positive'), ('negative', 'Negative')])
    def __str__(self):
        return f"Feedback for {self.event.title} by {self.user.username}"
