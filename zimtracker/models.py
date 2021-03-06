import datetime

from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class City(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Port(models.Model):

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_vessels(self):
        vessels = Vessel.objects.filter(log__dest_port=self)
        return vessels.distinct()

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
    dest_port = models.ForeignKey(Port,
        on_delete=models.SET_NULL, blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    blocked_days = models.IntegerField(default=0)

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
    status = models.IntegerField(blank=True, null=True)
    dsrc = models.CharField(max_length=255, blank=True)
    flag = models.CharField(max_length=255, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    dest_port = models.ForeignKey(Port, 
        on_delete=models.SET_NULL, blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    time_collected = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp', 'vessel')

    def __str__(self):
        return '{}: {}'.format(self.vessel.name, self.timestamp)

    def get_fields(self):
        return ('mmsi', 'speed', 'heading', 'course', 
            'status', 'latitude', 'longitude', 'dsrc', 
            'flag', 'destination', 'eta')

    def get_field_type_dict(self):
        return {'int': int, 'dec': Decimal, 'char': str}

    def get_int_fields(self):
        return ('mmsi', 'speed', 'heading', 'course', 
            'status')

    def get_dec_fields(self):
        return ('latitude', 'longitude')

    def get_char_fields(self):
        return ('dsrc', 'flag', 'destination',)

    def get_date_fields(self):
        return ('eta',)

    def get_speed(self):
        if self.speed:
            return self.speed / 10
        return ''

    def get_epoch_time(self):
        return self.timestamp.timestamp()

    def get_opacity(self):
        logs = self.vessel.log_set.order_by('timestamp')
        i = 0
        for log in logs:
            i +=1
            if log == self:
                return i / logs.count()

class UserProfile(models.Model):

    user = models.OneToOneField(User, 
        on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    ships = models.ManyToManyField(Vessel, blank=True)
    ports = models.ManyToManyField(Port, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()