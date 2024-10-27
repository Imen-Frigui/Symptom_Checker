from django.contrib import admin
from .models import Symptom, Illness

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Illness)
class IllnessAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('symptoms',)
