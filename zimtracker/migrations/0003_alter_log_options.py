# Generated by Django 3.2.3 on 2021-05-24 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zimtracker', '0002_auto_20210524_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': ('-timestamp', 'vessel')},
        ),
    ]
