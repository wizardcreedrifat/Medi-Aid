from django.contrib import admin
from .models import Doctor, Patient, InsuranceProvider, Prescription, Appointment, Comission
# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'number', 'gender', 'qualification', 'speciality', 'hospital', 'availability','percentage', 'start', 'end', 'profilepic')
    list_filter = ('id','number')
    search_fields = ('id','name', 'number')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'insurance', 'number', 'gender', 'blood', 'birthdate', 'medications', 'disease', 'allergy', 'profilepic')
    list_filter = ('id','number')
    search_fields = ('id','name', 'number')

class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ('id','name',  'number', 'address', 'policy')
    list_filter = ('id','number')
    search_fields = ('id','name', 'number')

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id','users', 'doctor', 'patient', 'disease', 'date', 'hospital', 'upload', 'presctext')
    list_filter = ('id','users', 'doctor', 'patient')
    search_fields = ('id','users', 'doctor', 'patient')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'doctor_name', 'patient_name', 'disease', 'email', 'phone', 'payment', 'expected_date', 'expected_time', 'expected_date', 'accepted')
    list_filter = ('id', 'doctor', 'patient', 'expected_date', 'expected_time', 'accepted')
    search_fields = ('id', 'doctor', 'patient', 'doctor_name', 'patient_name', 'expected_date', 'expected_time', 'accepted')    

class ComissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient_num', 'total_earnings', 'percentage')
    list_filter = ('id', 'doctor')
    search_fields = ('id', 'doctor')


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient,PatientAdmin)
admin.site.register(InsuranceProvider, InsuranceProviderAdmin)
admin.site.register(Prescription,PrescriptionAdmin)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Comission,ComissionAdmin)
