from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    patronymic_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    university = models.CharField(max_length=100, blank=True)
    university_faculty = models.CharField(max_length=100, blank=True)
    university_specitality = models.CharField(max_length=100, blank=True)

    COURSES = [
        ('2 курс', '2 курс'),
        ('3 курс', '3 курс')
    ]
    university_course = models.CharField(max_length=100, choices=COURSES, blank=True)

    TEST = [
        ('ONE ОДИН', 'ONE ОДИН'),
        ('TWO ОДИН', 'TWO ОДИН'),
    ]
    school_program = models.CharField(max_length=100, choices=TEST, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()