from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.core.urlresolvers import reverse

# Create your models here.
class Room(models.Model):
    name=models.TextField()
    label=models.SlugField(unique=True)
    users=models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('chat:ENTER', args=(self.label, ))

class Message(models.Model):
    room=models.ForeignKey(Room, related_name="messages")
    handle=models.TextField()
    message=models.TextField()
    timestamp=models.DateTimeField(default=timezone.now)

    def as_dict(self):
        return {"handle":self.handle, "message":self.message, "timestamp":self.timestamp}

    def __str__(self):
        return "[{timestamp}] {handle}: {message}".format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%b %-d %-I:%M %p")

