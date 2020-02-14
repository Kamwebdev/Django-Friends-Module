from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", blank=True)
    liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked", blank=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "Owner: " + self.owner.first_name + ", Liked user:" + self.liked.first_name + ", Accepted: " + str(self.accepted)
