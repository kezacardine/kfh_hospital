from django.contrib import admin
from .models import Patient, VitalSign

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'first_name', 'last_name', 'gender', 'phone', 'created_at']
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone']
    list_filter = ['gender', 'created_at']
    ordering = ['-created_at']

@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ['patient', 'heart_rate', 'temperature', 'systolic_bp', 'diastolic_bp', 'recorded_at']
    list_filter = ['recorded_at', 'recorded_by']
    search_fields = ['patient__patient_id', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'recorded_at'
    ordering = ['-recorded_at']