from django.db import models

class Consultation(models.Model):
    doctor_name = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    consultation_date = models.DateTimeField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.doctor_name} - {self.patient_name}"


