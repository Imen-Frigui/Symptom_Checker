from django.contrib import admin
from .models import Medication, SideEffect, Treatment

# Register your models here.
admin.site.register(Medication)
admin.site.register(SideEffect)
admin.site.register(Treatment)
