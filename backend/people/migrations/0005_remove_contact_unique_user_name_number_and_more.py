# Generated by Django 4.0.2 on 2022-04-03 19:11

import choices.time
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0004_event_remove_contact_birthday_contact_source_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='contact',
            name='unique_user_name_number',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='user',
        ),
        migrations.AddField(
            model_name='contact',
            name='created_by',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contact',
            name='last_modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='frequency',
            field=models.CharField(choices=[('None', 'Once'), ('1D', 'Daily'), ('7D', 'Weekly'), ('1M', 'Monthly'), ('1Y', 'Yearly')], default=choices.time.Frequency['ONCE'], max_length=25),
        ),
        migrations.AddField(
            model_name='event',
            name='last_modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contact',
            name='source',
            field=models.CharField(blank=True, default='Manual', editable=False, max_length=25),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(django.db.models.expressions.F('created_by'), django.db.models.functions.text.Lower('name'), django.db.models.expressions.F('number'), name='unique_created_by_name_number'),
        ),
    ]
