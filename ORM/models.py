from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ResetID(models.Model):
    UUID = models.UUIDField(unique=True)
    reset_entry = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
