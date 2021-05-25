import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Vessel(models.Model):

    name = models.CharField(max_length=255, blank=True)
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

    def get_absolute_url(self):
        return reverse('vessel-detail', kwargs={'pk':self.id})

    def get_log(self):
        logs = self.log_set.order_by('-timestamp')
        if logs:
            return logs[0]
        return None

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
    dsrc = models.CharField(max_length=255, blank=True)
    flag = models.CharField(max_length=255, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    eta = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    time_collected = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp', 'vessel')

    def __str__(self):
        return '{}: {}'.format(self.vessel.name, self.timestamp)

    def get_mt_fields(self):
        return ('mmsi', 'latitude', 'longitude', 'speed', 
            'heading', 'course', 'source', 'flag', 'status', 
            'dsrc', 'destination', 'eta')

    def get_speed(self):
        if self.speed:
            return self.speed / 10
        return ''

    def get_epoch_time(self):
        return self.timestamp.timestamp()

class UserProfile(models.Model):

    user = models.OneToOneField(User, 
        on_delete=models.CASCADE)
    ships = models.ManyToManyField(Vessel, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()