# Generated by Django 4.0.2 on 2022-03-12 16:20

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(default=0, max_length=128, region=None),
            preserve_default=False,
        ),
    ]