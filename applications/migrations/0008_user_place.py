# Generated by Django 3.2.25 on 2024-11-09 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='applications.place'),
        ),
    ]
