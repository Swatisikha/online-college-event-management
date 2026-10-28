from django.db import models
from django.conf import settings

# Create your models here.



class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=200)

    registration_deadline = models.DateField(
        null=True,
        blank=True
    )

    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Registration(models.Model):
    student = models.ForeignKey(
    settings.AUTH_USER_MODEL,

    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    college_roll_number = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name    
