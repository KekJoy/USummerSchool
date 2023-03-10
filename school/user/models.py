from django.db import models
from authentication.models import Profile


class ProgramList(models.Model):
    title = models.CharField(max_length=200)


class TaskList(models.Model):
    program = models.ForeignKey(ProgramList, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()


class Programs(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    program_list = models.ForeignKey(ProgramList, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


class TaskAnswer(models.Model):
    task = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    programs = models.ForeignKey(Programs, on_delete=models.CASCADE)
    answer = models.TextField()

    GRADES = [
        ('A', '5'),
        ('B', '4'),
        ('C', '3'),
        ('D', '2'),
        ('F', '1'),
    ]
    grade = models.CharField(max_length=1, choices=GRADES)
