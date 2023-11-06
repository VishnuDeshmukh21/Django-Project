from django.db import models
from django.conf import settings

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
  uid = models.CharField(max_length=255, null=True, blank=True)
  
  def __str__(self):
    return f'{self.user.username} Profile'