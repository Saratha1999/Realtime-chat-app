from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
    
class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed_users = models.ManyToManyField(User, related_name='allowed_rooms', blank=True)


    def __str__(self):
        return self.name

