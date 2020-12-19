from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.
class Pizza(models.Model):
    SIZE = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    TYPES = (
        ('S', 'Square'),
        ('R', 'Regular')
    )
    size = models.CharField(blank=False, max_length=1, choices=SIZE)
    types = models.CharField(blank=False, max_length=1, choices=TYPES)
    toppings = JSONField(blank=True)

    class Meta:
        db_table = 'pizza'