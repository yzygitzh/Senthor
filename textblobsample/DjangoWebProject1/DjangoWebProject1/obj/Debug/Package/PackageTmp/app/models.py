"""
Definition of models.
"""

from django.db import models

# Create your models here.
class PersonInfo(models.Model):
    name = models.CharField(max_length=32)
    age=models.IntegerField()
    gender=models.BinaryField()
    email=models.CharField(max_length=32)


