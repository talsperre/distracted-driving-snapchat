from django.db import models
from django.contrib.auth.models import User

class OTP(models.Model):

    email = models.CharField(max_length=255)
    otp = models.CharField(max_length=10)

    def __str__(self):
        return str(self.email) + ": " + str(self.otp)
