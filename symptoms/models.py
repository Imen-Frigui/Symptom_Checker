from django.db import models

class Symptom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=50,  null=True)  # e.g., 'mild', 'moderate', 'severe'

    def __str__(self):
        return self.name

class Illness(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    symptoms = models.ManyToManyField(Symptom, related_name='illnesses')

    def __str__(self):
        return self.name
