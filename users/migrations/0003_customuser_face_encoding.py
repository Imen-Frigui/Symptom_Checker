# Generated by Django 4.2 on 2024-10-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='face_encoding',
            field=models.TextField(blank=True, null=True),
        ),
    ]
