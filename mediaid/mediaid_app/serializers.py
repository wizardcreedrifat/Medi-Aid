from rest_framework import serializers
from .models import InsuranceProvider, Doctor, Patient, Prescription, Appointment, User, Comission
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import authenticate, get_user_model

UserModel = User()


class NewUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields=["email","id","username"]

class NewRegisterSerializer(RegisterSerializer):
    pass

class NewLoginSerializer(LoginSerializer):
    pass

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'   

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'   

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'   


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'   


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class ComissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comission
        fields = '__all__'   
