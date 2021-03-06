# Generated by Django 4.0.2 on 2022-04-02 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0004_event_remove_contact_birthday_contact_source_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='Hi')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('time_to_send', models.DateTimeField(default=django.utils.timezone.now)),
                ('sent', models.BooleanField(default=True)),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.contact')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='scheduledmessage',
            constraint=models.CheckConstraint(check=models.Q(('contact__isnull', False), ('number__isnull', False), _connector='OR'), name='not_both_null'),
        ),
    ]
