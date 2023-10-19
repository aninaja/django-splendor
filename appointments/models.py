from datetime import datetime
from django.db import models
from django.utils import timezone
from treatments.models import Treatment
from user_profile.models import User


# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField(null=False, blank=True)
    TIME_CHOICES = [
        ("------", "------"),
        ("10 AM", "10 AM"),
        ("11 AM", "11 AM"),
        ("12 PM", "12 PM"),
        ("1 PM", "1 PM"),
        ("2 PM", "2 PM"),
        ("3 PM", "3 PM"),
        ("4 PM", "4 PM"),
        ("5 PM", "5 PM"),
        ("6 PM", "6 PM"),
        ("7 PM", "7 PM"),
        ("8 PM", "8 PM"),
        ("9 PM", "9 PM"),
    ]
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    treatment = models.ForeignKey(Treatment, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"{self.date} {self.time}"

    class Meta:
        db_table = 'appointments'
