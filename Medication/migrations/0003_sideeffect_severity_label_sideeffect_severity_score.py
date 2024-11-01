# Generated by Django 4.2 on 2024-10-26 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medication', '0002_remove_prescription_medications_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sideeffect',
            name='severity_label',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sideeffect',
            name='severity_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
