from django.apps import apps
from django.conf import settings
from marinetrafficapi import MarineTrafficApi

from .models import Vessel

Vessel = apps.get_model(app_label='zimtracker', 
    model_name='Vessel')
Log = apps.get_model(app_label='zimtracker', 
    model_name='Log')

def update_vessels():
    api = MarineTrafficApi(
        api_key=settings.MARINETRAFFIC_API_KEY)
    vessels = api.fleet_vessel_positions(time_span=60, 
        msg_type='extended')
    for vessel in vessels.models:
        print('updating vessel')
        update_vessel_data(vessel)

def update_vessel_data(v_data):
    ship_id = v_data.ship_id.value
    vessel, created = Vessel.objects.get_or_create(
        ship_id=ship_id)
    if created:
        print('Added ship {}'.format(ship_id))
        vessel.imo = v_data.imo.value
        if v_data.ship_name.value:
            vessel.name = v_data.ship_name.value
        vessel.save()
    log, created = Log.objects.get_or_create(
        vessel=vessel,timestamp=v_data.timestamp.value)
    if created:
        for field in log.get_mt_fields():
            if getattr(v_data, field, None):
                setattr(log, field, getattr(v_data,field))
        log.save()
        print('Log created')






