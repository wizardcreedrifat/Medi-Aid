from django.db import models
from django.contrib.auth.models import User
# Create your models here.

Gender = (
    ('Male','Male'),
    ('Female','Female'),
    ('male','male'),
    ('female','female'),
    ('Others','Othes'))

Payment = (
    ('On-Site','On-Site'),
    ('Online','Online'),
    ('online','online'),
    ('on-site','on-site'),
    ('onsite','onsite'),
    ('Onsite','Onsite'))

class InsuranceProvider(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    policy = models.TextField()



class Doctor(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    gender = models.CharField(choices=Gender, default='choose one', max_length=10)
    number = models.CharField(max_length=20)
    licensenum = models.CharField(max_length=30)
    hospital = models.CharField(max_length=50)
    speciality = models.TextField(max_length=100)
    qualification = models.TextField(max_length=100)
    availability = models.CharField(max_length=20)
    start = models.TimeField()
    end = models.TimeField()
    fees = models.CharField(max_length=5)
    percentage = models.CharField(max_length=20)
    profilepic = models.FileField(blank=True, null=True)



class Patient(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    insurance = models.CharField(max_length=10, default=-1, blank=True, null=True)
    name = models.CharField(max_length=40)
    number = models.CharField(max_length=20)
    birthdate = models.DateField()
    blood = models.CharField(max_length=10)
    gender = models.CharField(choices=Gender, default='choose one', max_length=10)
    medications = models.TextField()
    disease = models.TextField()
    allergy = models.TextField()
    profilepic = models.FileField(blank=True, null=True)



class Prescription(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.TextField()
    date = models.DateField(auto_now_add=True)
    hospital = models.CharField(max_length=50)
    upload = models.FileField()
    presctext = models.TextField()


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=30)
    patient_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    disease = models.TextField(blank=True)
    expected_date = models.DateField()
    expected_time = models.TimeField()
    payment = models.CharField(choices=Payment, default='On-Site', max_length=10)
    requested_at = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

class Comission(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    patient_num = models.PositiveIntegerField(default=0, blank=True)
    total_earnings = models.PositiveIntegerField(blank=True)
    percentage = models.CharField(max_length=20)


