# Generated by Django 4.0.2 on 2022-04-02 12:58

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_contact_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='contact',
            name='birthday',
        ),
        migrations.AddField(
            model_name='contact',
            name='source',
            field=models.CharField(db_column='source', default='Manual', max_length=25),
        ),
        migrations.AlterField(
            model_name='contact',
            name='detail',
            field=models.TextField(default='Manually made contact'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(django.db.models.expressions.F('user'), django.db.models.functions.text.Lower('name'), django.db.models.expressions.F('number'), name='unique_user_name_number'),
        ),
        migrations.AddField(
            model_name='event',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.contact'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(django.db.models.expressions.F('contact'), django.db.models.functions.text.Lower('name'), django.db.models.expressions.F('date'), name='unique_contact_name_date'),
        ),
    ]
