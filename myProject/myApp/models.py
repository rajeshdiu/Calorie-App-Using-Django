from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student')
    ]
    display_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=120)
    otp_token = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, null=True)
    height = models.FloatField()
    weight = models.FloatField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class ConsumedCalories(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    calorie_consumed = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} consumed {self.calorie_consumed} calories on {self.date}"
