""" # institutions/admin.py

from django.contrib import admin
from .models import HealthCareInstitution

@admin.register(HealthCareInstitution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')
 """