import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Vessel(models.Model):

    name = models.CharField(max_length=255)
    imo = models.IntegerField(blank=True, null=True)
    ship_id = models.IntegerField(blank=True, null=True)
    mmsi = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, 
        decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, 
        decimal_places=6, blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    heading = models.IntegerField(blank=True, null=True)
    course = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True)
    flag = models.CharField(max_length=255, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    eta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Log(models.Model):
    vessel = models.ForeignKey(Vessel, 
        on_delete=models.CASCADE)
    mmsi = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, 
        decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, 
        decimal_places=6, blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    heading = models.IntegerField(blank=True, null=True)
    course = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True)
    flag = models.CharField(max_length=255, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    eta = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    time_collected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {}'.format(self.name, self.timestamp)

class UserProfile(models.Model):

    user = models.OneToOneField(User, 
        on_delete=models.CASCADE)
    ships = models.ManyToManyField(Vessel, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()