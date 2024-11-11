# Generated by Django 3.2.25 on 2024-11-09 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_alter_application_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='design_image',
            field=models.ImageField(blank=True, null=True, upload_to='admin/'),
        ),
    ]