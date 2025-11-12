from django.db import models
from django.contrib.auth.models import User

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Event Model
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField(auto_now=True)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    image = models.ImageField(upload_to='events/',default='default.jpg')

    participants = models.ManyToManyField(User,through='RSVP',related_name='rsvped_events')

    def __str__(self):
        return self.name

class RSVP(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    rsvp_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Confirmed","Confirmed"), ("Attended","Attended")], default="Confirmed")

    class Meta:
        unique_together = ('user','event')
