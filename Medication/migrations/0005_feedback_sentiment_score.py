# Generated by Django 4.2 on 2024-10-27 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medication', '0004_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='sentiment_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
