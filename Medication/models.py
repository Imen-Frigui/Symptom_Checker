from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='medications/', blank=True, null=True)
    side_effects = models.ManyToManyField('SideEffect', related_name='medications', blank=True)

    def __str__(self):
        return self.name

class SideEffect(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    medications = models.ManyToManyField(Medication, related_name='treatments', blank=True)

    def __str__(self):
        return self.name
