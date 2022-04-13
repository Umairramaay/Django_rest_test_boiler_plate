from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from patients.models import *

@admin.register(Patient)
class PatientDataAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'owner_name',
        'pet_name',
        'owner_phone_number',
    ]
    list_filter = [
        'owner_phone_number',
        'pet_name',
        'owner_name'
    ]
    search_fields = [
        'owner_name',
        'owner_phone_number',
        'pet_name'
    ]
    
@admin.register(Appointment)
class AppointmentaAdmin(admin.ModelAdmin):
    
    def patient_link(self, obj):
        if obj.patient:
            link = reverse("admin:patients_patient_change", args=[obj.patient.id])
            return format_html(u'<a href="%s">%s</a>' % (link, obj.patient.pet_name))
        return None
    patient_link.allow_tags = True
    patient_link.short_description = 'Patient'

    list_display = [
        'id',
        'patient_link',
        'start_time',
        'end_time',
    ]
    list_filter = [
        'patient',
        'end_time',
        'end_time'
    ]
    search_fields = [
        'patient__owner_name',
        'patient__et_name'
    ]