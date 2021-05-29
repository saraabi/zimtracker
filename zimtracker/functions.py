from django.apps import apps
from django.conf import settings

from marinetrafficapi import MarineTrafficApi
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

from .models import Vessel

Vessel = apps.get_model(app_label='zimtracker', 
    model_name='Vessel')
Log = apps.get_model(app_label='zimtracker', 
    model_name='Log')

def update_vessels():
    api = MarineTrafficApi(
        api_key=settings.MARINETRAFFIC_API_KEY)
    try:
        vessels = api.fleet_vessel_positions(time_span=60, 
            msg_type='extended')
        print('Extended Data')
    except:
        vessels = api.fleet_vessel_positions(time_span=60)
        print('Basic Data')
    print(vessels.meta)
    for vessel in vessels.models:
        print('updating vessel')
        update_vessel_data(vessel)
    return vessels

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
    # if created:
    for field in log.get_fields():
    # for key, func in log.get_field_type_dict().items():
    #     method = 'get_{}_fields'.format(key)
    #     for field in getattr(log, method)():
        value = getattr(v_data, field, None)
        if value.value:
            print(field, value.value)
            setattr(log, field, value.value)
    # log.eta = getattr(v_data, 'eta', None)
    log.save()
    if created:
        send_updates(log)
    print('Log created')

def send_updates(log):
    api_key = settings.TWILIO_API_KEY
    secret = settings.TWILIO_SECRET_KEY
    phone = settings.TWILIO_PHONE
    client = Client(api_key, secret)
    body = '[Ship Update] The {} has an updated status: \
        https://zimtracker.herokuapp.com/vessels/{}'.format(
        log.vessel.name, log.vessel.id
    )
    kwargs = {'from_': phone, 'body': body}
    for user in log.vessel.userprofile_set.all():
        kwargs['to'] = user.phone
        client.messages.create(**kwargs)

def send_email(to, subject, content):
    message = Mail(
        from_email='admin@zimtracker.herokuapp.com',
        to_emails=to,
        subject=subject,
        html_content=content)
    try:
        api_key = settings.SENDGRID_API_KEY
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print('ERROR')
        print(e)
        print(e.message)

