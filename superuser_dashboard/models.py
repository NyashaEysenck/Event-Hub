from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    """Model for Event Categories (Optional - if managing categories as separate entities)"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Category model (if applicable)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the event

    def __str__(self):
        return self.title