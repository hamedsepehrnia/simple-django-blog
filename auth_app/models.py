from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    occupation = models.TextField()
    website = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.user.username