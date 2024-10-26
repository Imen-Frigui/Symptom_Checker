from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class HealthCareInstitution(models.Model):
    INSTITUTION_TYPES = [
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('pharmacy', 'Pharmacy'),
        ('diagnostic_center', 'Diagnostic Center'),
    ]

    name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=50, choices=INSTITUTION_TYPES)
    location = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    operational_hours = models.JSONField(blank=True, null=True)
    services_provided = models.TextField(blank=True)
    insurance_accepted = models.TextField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        null=True
    )
    capacity = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Health Care Institutions"
