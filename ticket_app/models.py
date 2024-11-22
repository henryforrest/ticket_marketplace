from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.conf import settings


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # This means if the user is deleted, their tickets will be deleted
        related_name='tickets_sold', 
        default = 1
    )
    sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        related_name='tickets_bought', 
        default = 0,
        null=True,  # Allow NULL values
        blank=True
    )


    def __str__(self):
        return f"{self.event} on {self.date} at {self.time} - ${self.price}"

class UserProfile(AbstractUser):
    
    pass

