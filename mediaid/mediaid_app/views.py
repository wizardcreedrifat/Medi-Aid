from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.views import View
import pytesseract
from PIL import Image
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import User, Doctor, Patient, Prescription, InsuranceProvider, Appointment, Comission
from .forms import *
import os, openai
from PIL import Image
from django.conf import settings
from django.core.mail import EmailMessage
from datetime import datetime 
from django.views.generic import ListView
from django.template import context
from django.template.loader import render_to_string, get_template
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import json
import io
from .serializers import InsuranceSerializer, DoctorSerializer, PatientSerializer, PrescriptionSerializer, AppointmentSerializer, ComissionSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.views.decorators.csrf  import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from sslcommerz_lib import SSLCOMMERZ 
from decimal import Decimal


api_key = os.environ.get("OPENAI_KEY")
openai.api_key = api_key


# Create your views here.
def LandingPage(request):
    return render(request, 'mediaid/LandingPage.html')






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Home(request):
    return render(request, 'mediaid/home.html')






def Services(request):
    return render(request, 'mediaid/services.html')







class ContactUs(View):
    def get(self,request):
        return render(request, 'mediaid/contactus.html')
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('msg')

        email = EmailMessage(
            subject = f"{name} from MediAid",
            body = msg,
            from_email = settings.EMAIL_HOST_USER,
            to = [settings.EMAIL_HOST_USER],
            reply_to = [email]
        )
        email.send()
        messages.success(request, 'Your Feedback Submitted Successfully')
        return render(request, 'mediaid/contactus.html',{'message':messages})









@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ProfilePage(request):
    usr = request.user
    try:
        doc = Doctor.objects.get(users_id=usr.id)
    except:
        doc = None
    if(doc!=None):
        return render(request, 'mediaid/profile.html',{'usr':usr,'doc':doc ,'active':'btn-info'})
    else:        
        return render(request, 'mediaid/profile.html',{'usr':usr,'active':'btn-info'})








class RegistrationView(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request, 'mediaid/register.html' , {'form':form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Congratulations!! Successfully Registered')
            except:
                messages.success(request, 'Sorry!! Could not be Registered, Try Again')
        return render(request, 'mediaid/register.html' , {'form':form})
    











@method_decorator(login_required, name='dispatch')
class DocRegistration(View):
    def get(self,request):
        form = DoctorForm()
        return render(request, 'mediaid/doctorreg.html',{'form':form})
    def post(self, request):
        if request.method == "POST" and request.FILES['propic']:
            usr = request.user
            uid = usr.id
            name = request.POST['name']
            number = request.POST['num']
            gender = request.POST['gender']
            hospital = request.POST['hospital']
            qualification = request.POST['qualification']
            speciality = request.POST['speciality']
            availability = request.POST['availability']
            start = request.POST['start']
            end = request.POST['end']
            fees = request.POST['fees']
            percentage = request.POST['comission'] 
            propic = request.FILES['propic']
            try:
                inr = Doctor.objects.get(users_id=uid)
            except Doctor.DoesNotExist:
                inr = None
            if(inr!=None):
                messages.warning(request, 'user id already exists')
                return render(request, 'mediaid/doctorreg.html', {'message':messages})
            else:
                reg = Doctor(users_id=uid ,name=name, number=number, gender=gender, hospital=hospital, qualification=qualification, 
                speciality=speciality, availability=availability, start=start, end=end, fees=fees, percentage=percentage, profilepic=propic)
                reg.save()
                com = Comission(doctor = reg, patient_num = 0, total_earnings = 0, percentage = percentage)
                com.save()
                messages.success(request, 'Congratulations!! Successfully registered as a doctor')
                return render(request, 'mediaid/doctorreg.html', {'message':messages})












@method_decorator(login_required, name='dispatch')
class InsuranceProviderReg(View):
    def get(self,request):
        form = InsuranceRegForm()
        return render(request, 'mediaid/insurancereg.html' , {'form':form})
    def post(self, request):
        form = InsuranceRegForm(request.POST)
        if form.is_valid():
            usr = request.user
            uid = usr.id
            number = form.cleaned_data['number']
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            policy = form.cleaned_data['policy']
            try:
                inr = InsuranceProvider.objects.get(users_id=uid)
            except InsuranceProvider.DoesNotExist:
                inr = None
            if(inr!=None):
                messages.warning(request, 'User id already exists')
                return render(request, 'mediaid/insurancereg.html', {'message':messages})       
            else:         
                reg = InsuranceProvider(users_id=uid, name=name,number=number, address=address, policy=policy)
                reg.save()
                messages.success(request, 'Congratulations!! Successfully Registered')
                return render(request, 'mediaid/insurancereg.html' , {'form':form})
        else:
            messages.warning(request, 'Sorry!! Invalid Form Content')
            return render(request, 'mediaid/insurancereg.html' , {'form':form})
        











@method_decorator(login_required, name='dispatch')
class PatRegistration(View):
    def get(self,request):
        ins = InsuranceProvider.objects.all()
        return render(request, 'mediaid/patientreg.html',{'ins':ins})
    def post(self, request):
        if request.method == "POST" and request.FILES['propic']:
            usr = request.user
            uid = usr.id
            name = request.POST['name']
            insurance = request.POST['insurance']
            number = request.POST['num']
            gender = request.POST['gender']
            birthdate = request.POST['birthday']
            blood = request.POST['blood']
            medication = request.POST['medication']
            disease = request.POST['disease']
            allergy = request.POST['allergy']
            profilepic = request.FILES['propic']
            ins = InsuranceProvider.objects.all()
            if len(insurance)>0:
                insp = InsuranceProvider.objects.filter(id__icontains=insurance)
                if(insp):
                    try:
                        inr = Patient.objects.get(users_id=uid)
                    except Patient.DoesNotExist:
                        inr = None
                    if(inr!=None):
                        messages.warning(request, 'user id already exists')
                        return render(request, 'mediaid/patientreg.html', {'message':messages, 'ins':ins})
                    else:  
                        reg = Patient(users_id=uid ,name=name, number=number, gender=gender, insurance=insurance, medications=medication, 
                                disease=disease, birthdate=birthdate, blood=blood, allergy=allergy, profilepic=profilepic)
                        reg.save()
                        messages.success(request, 'Congratulations!! Successfully registered as a patient')
                        return render(request, 'mediaid/patientreg.html', {'message':messages, 'ins':ins})
                else:
                    messages.warning(request, 'Insurance does not company exist')
                    return render(request, 'mediaid/patientreg.html', {'message':messages, 'ins':ins})
            else:
                insurance = -1
                try:
                    inr = Patient.objects.get(users_id=uid)
                except Patient.DoesNotExist:
                    inr = None
                if(inr!=None):
                    messages.warning(request, 'user id already exists')
                    return render(request, 'mediaid/patientreg.html', {'message':messages, 'ins':ins})
                else:  
                    reg = Patient(users_id=uid ,name=name, number=number, gender=gender, insurance=insurance, medications=medication, 
                    disease=disease, birthdate=birthdate, blood=blood, allergy=allergy, profilepic=profilepic)
                    reg.save()
                    messages.success(request, 'Congratulations!! Successfully registered as a patient')
                    return render(request, 'mediaid/patientreg.html', {'message':messages, 'ins':ins})








@method_decorator(login_required, name='dispatch')
class AppointmentView(View):
    
    def get(self,request):
        doc = Doctor.objects.all()
        usr = request.user
        try:
            pat = Patient.objects.filter(users_id=usr.id)
        except:
            pat = None
        return render(request, 'mediaid/appointment1.html',{'doc':doc, 'pat':pat})
    
    def post(self, request):
        name = request.POST.get('pname')
        email = request.POST.get('pmail')
        pnum= request.POST.get('pnum')
        dname = request.POST.get('dname')
        did = request.POST.get('did')
        disease = request.POST.get('disease')
        date = request.POST.get('date')
        time = request.POST.get('time')
        payment = request.POST.get('paymentmethod')
        time = datetime.strptime(time, '%H:%M').time()
        doc = Doctor.objects.all()
        try:
            d = Doctor.objects.get(id=did)
            # if(d.name==dname):
            #     d = d
            # else:
            #     print("didnot")
            #     d = None
        except Doctor.DoesNotExist:
            messages.warning(request, "Doctor not found")
            return render(request, 'mediaid/appointment1.html',{'doc':doc})
        try:
            usr = request.user
            uid = usr.id
            p = Patient.objects.get(users_id=uid)
        except Patient.DoesNotExist:
            messages.warning(request, "Patient not found!! First register as a patient")
            return render(request, 'mediaid/appointment1.html',{'doc':doc})
        if(d!=None):
            if((time>d.start and time<d.end) or time==d.start):
                if(payment == "onsite"):
                    appointment = Appointment.objects.create(
                        doctor = d,
                        patient = p,
                        doctor_name = dname,
                        patient_name = name,
                        email = email,
                        phone = pnum,
                        disease = disease,
                        expected_date = date,
                        expected_time = time,
                        payment = payment 
                    )
                    appointment.save()
                    messages.success(request, "Appointment request submitted")
                    return render(request, 'mediaid/appointment1.html',{'doc':doc})
                else:
                    store_id = settings.SSLCOMMERZ_STORE_ID
                    store_pass = settings.SSLCOMMERZ_STORE_PASSWORD
                    status_url = request.build_absolute_uri(reverse('sslc_status'))


                    ssl_settings = { 'store_id': store_id, 'store_pass': store_pass, 'issandbox': True }
                    sslcommez = SSLCOMMERZ(ssl_settings)
                    post_body = {}
                    post_body['total_amount'] = d.fees
                    post_body['currency'] = "BDT"
                    post_body['tran_id'] = "12345"
                    post_body['success_url'] = status_url
                    post_body['fail_url'] = status_url
                    post_body['cancel_url'] = status_url
                    post_body['emi_option'] = 0
                    post_body['cus_name'] = name
                    post_body['cus_email'] = email
                    post_body['cus_phone'] = pnum
                    post_body['cus_add1'] = "customer address"
                    post_body['cus_city'] = "Dhaka"
                    post_body['cus_country'] = "Bangladesh"
                    post_body['shipping_method'] = "NO"
                    post_body['multi_card_name'] = ""
                    post_body['num_of_item'] = 1
                    post_body['product_name'] = "Appointment"
                    post_body['product_category'] = "Test Category"
                    post_body['product_profile'] = "general"
                    response = sslcommez.createSession(post_body)

                    if response['status'] == 'SUCCESS':
                        appointment = Appointment.objects.create(
                            doctor = d,
                            patient = p,
                            doctor_name = dname,
                            patient_name = name,
                            email = email,
                            phone = pnum,
                            disease = disease,
                            expected_date = date,
                            expected_time = time,
                            payment = payment 
                        )
                        appointment.save()
                        com = Comission.objects.get(doctor=d)
                        com.patient_num = com.patient_num+1
                        com.total_earnings = com.total_earnings+int(d.fees)
                        com.save()
                        messages.success(request, "Appointment request submitted")
                        return redirect(response['GatewayPageURL'])
                    else:
                        messages.warning(request, "Payment Unsuccessfull")
                        return render(request, 'mediaid/appointment1.html',{'doc':doc})
            else:
                messages.warning(request, "Choose an appropriate time")
                return render(request, 'mediaid/appointment1.html',{'doc':doc, 'pat':p})
        else:
            messages.warning(request, "Fill the form carefully with appropriate informations")
            return render(request, 'mediaid/appointment1.html',{'doc':doc, 'pat':p})


@csrf_exempt
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            trans_id = payment_data['tran_id']
            return(HttpResponseRedirect(reverse('sslc_complete', kwargs={'val_id':val_id, 'tran_id':trans_id})))
        else:
            usr = request.user
            doc = Doctor.objects.all()
            messages.warning(request, "Payment Unsuccessfull")
            return render(request, 'mediaid/appointment1.html',{'doc':doc})



def sslc_complete(request, val_id, tran_id):
    usr = request.user
    doc = Doctor.objects.all()
    messages.warning(request, "Payment Successfull")
    return render(request, 'mediaid/appointment1.html',{'doc':doc})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Appointment_View(request, id):
    if request.method == 'POST':
        d = Doctor.objects.get(id=id)
        name = request.POST.get('pname')
        email = request.POST.get('pmail')
        pnum= request.POST.get('pnum')
        dname = request.POST.get('dname')
        did = request.POST.get('did')
        disease = request.POST.get('disease')
        date = request.POST.get('date')
        time = request.POST.get('time')
        time = datetime.strptime(time, '%H:%M').time()
        doc = Doctor.objects.all()
        try:
            usr = request.user
            uid = usr.id
            p = Patient.objects.get(users_id=uid)
        except Patient.DoesNotExist:
            messages.warning(request, "Patient not found!! First register as a patient")
            return render(request, 'mediaid/appointment1.html',{'doc':doc, 'd':d})
        if(d!=None):
            if((time>d.start and time<d.end) or time==d.start):
                appointment = Appointment.objects.create(
                    doctor = d,
                    patient = p,
                    doctor_name = dname,
                    patient_name = name,
                    email = email,
                    phone = pnum,
                    disease = disease,
                    expected_date = date,
                    expected_time = time 
                )
                appointment.save()
                messages.success(request, "Appointment request submitted")
                return render(request, 'mediaid/appointment1.html',{'doc':doc, 'd':d})
            else:
                messages.warning(request, "Choose an appropriate time")
                return render(request, 'mediaid/appointment1.html',{'doc':doc, 'pat':p, 'd':d})
        else:
            messages.warning(request, "Fill the form carefully with appropriate informations")
            return render(request, 'mediaid/appointment1.html',{'doc':doc, 'pat':p, 'd':d})
    else:
        doc = Doctor.objects.all()
        d = Doctor.objects.get(id=id)
        return render(request, 'mediaid/appointment2.html',{'doc':doc, 'd':d})    







@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Appointment_List(request):
    usr = request.user
    try:
        doc = Doctor.objects.get(users_id=usr.id)
    except:
        doc = None
    try:
        pat = Patient.objects.get(users_id=usr.id)
    except:
        pat = None
    if(doc!=None):
        try:
            appd = Appointment.objects.filter(doctor= doc)
        except:
            appd = None
    else:
        appd = None
    if(pat!=None):
        try:
            appp = Appointment.objects.filter(patient= pat)
        except:
            appp = None
    else:
        appp = None
    if(appd!=None):
        if(appp!=None):
            return render(request, 'mediaid/appointlist.html',{'appd':appd,'appp':appp})
        else:
            return render(request, 'mediaid/appointlist.html',{'appd':appd})
    else:
        if(appp!=None):
            return render(request, 'mediaid/appointlist.html',{'appp':appp})
        else:
            return render(request, 'mediaid/appointlist.html')



           




@method_decorator(login_required, name='dispatch')
class ManageAppointment(View):
    model = Appointment
    context_object_name = "appointments"
    paginate_by = 3
    
    def get(self,request):
        usr = request.user
        doc = Doctor.objects.get(users_id=usr.id)
        try:
            app = Appointment.objects.filter(doctor=doc.id) & Appointment.objects.filter(accepted=False)
        except:
            app = None
        return render(request, 'mediaid/manage_appointment.html',{'app':app, 'active':'btn-info'})
    
    def post(self, request):
        date = request.POST.get("date")
        time = request.POST.get("time")
        app_id = request.POST.get("app-id")
        app = Appointment.objects.get(id=app_id)
        app.accepted = True
        app.expected_date = date
        app.expected_time = time
        app.save()
        data = {
            'pname':app.patient.name,
            'dname':app.doctor.name,
            'date':date,
            'time':time,
            'hos':app.doctor.hospital
        }
        msg = get_template('mediaid/email.html').render(data)

        email = EmailMessage(
            "About your appointment",
            msg,
            settings.EMAIL_HOST_USER,
            [app.email],
        )
        email.content_subtype = "html"
        email.send()
        messages.add_message(request, messages.SUCCESS, f"Appointment of {app.patient.name} is accepted")

        if app.payment == 'onsite':
            usr = request.user
            doc = Doctor.objects.get(users_id=usr.id)
            com = Comission.objects.get(doctor=doc)
            com.patient_num = com.patient_num+1
            com.total_earnings = com.total_earnings+int(doc.fees)
            com.save()
        try:
            appo = Appointment.objects.filter(doctor=doc.id) & Appointment.objects.filter(accepted=False)
        except:
            appo = None
        if(app!=None):
            return render(request, 'mediaid/manage_appointment.html',{'app':appo, 'active':'btn-info'})
        else:
            return render(request, 'mediaid/manage_appointment.html',{'app':appo, 'active':'btn-info'})







@method_decorator(login_required, name='dispatch')
class PrescriptionUp(View):
    def get(self,request):
        # form = PrescriptionUpForm()
        ins = Doctor.objects.all()
        return render(request, 'mediaid/prescriptionup.html' , {'ins':ins})
    def post(self, request):
        ins = Doctor.objects.all()
        if request.method == "POST" and request.FILES['upload']:
            usr = request.user
            uid = usr.id
            doctor = request.POST['doctor']
            disease = request.POST['disease']
            hospital = request.POST['hospital']
            upload = request.FILES['upload']
            text = ""
            try:
                inr = Doctor.objects.get(id=doctor)
            except Doctor.DoesNotExist:
                inr = None
            try:
                pat = Patient.objects.get(users_id=uid)
            except Patient.DoesNotExist:
                pat = None
            if(inr==None):
                messages.warning(request, 'Doctor does not exists')
                return render(request, 'mediaid/prescriptionup.html', {'message':messages, 'ins':ins})
            if(pat==None):
                messages.warning(request, 'First open patient id')
                return redirect('patient-registration')       
            # if(text==None):
            #     messages.warning(request, 'Could not convert prescription into text')
            #     return render(request, 'mediaid/prescriptionup.html', {'message':messages, 'ins':ins, 't':upload})
            else:         
                reg = Prescription(users_id=uid, doctor_id=doctor,patient_id=pat.id, disease=disease, hospital=hospital, upload=upload, presctext=text)
                reg.save()
                p = Prescription.objects.last()
                image_text = pytesseract.image_to_string(Image.open("media/"+p.upload.name))
                text = image_text
                try:
                    pr = Prescription.objects.get(id=p.id)
                    pr.presctext = text
                    pr.save()
                except Prescription.DoesNotExist:
                    pr = None
                # img_to_txt(p.upload, p.id)
                if(pr!=None):
                    messages.success(request, 'Congratulations!! Successfully Uploaded')
                    return render(request, 'mediaid/prescriptionup.html' , {'message':messages, 'ins':ins})
                else:
                    messages.warning(request, 'Sorry could not save the text')
                    return render(request, 'mediaid/prescriptionup.html' , {'message':messages, 'ins':ins})
        else:
            messages.warning(request, 'Sorry!! Invalid Form Content')
            return render(request, 'mediaid/prescriptionup.html' , {'message':messages, 'ins':ins})











@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def search_view(request):
    search = request.GET['search']
    if len(search)>0:
        doc = Doctor.objects.filter(name__icontains=search) | Doctor.objects.filter(id__icontains=search)
        pat = Patient.objects.filter(name__icontains=search) | Patient.objects.filter(id__icontains=search) 
        params = {'doc':doc, 'pat':pat}
        return render(request,'mediaid/doctorslist.html', params)
    else:
        return render(request,'mediaid/doctorslist.html')












@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def patientsearch_view(request):
    return render(request, 'mediaid/patientlist.html')










@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def docprofile(request):
    usr = request.user
    uid = usr.id
    try:
        doc = Doctor.objects.get(users_id=uid)
    except Doctor.DoesNotExist:
        doc = None
    if(doc!=None):
        return render(request, 'mediaid/docprofile.html',{'doc':doc})
    else:
        return render(request, 'mediaid/docprofile.html')










@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def patprofile(request):
    usr = request.user
    uid = usr.id
    try:
        pat = Patient.objects.get(users_id=uid)
    except Patient.DoesNotExist:
        pat = None
    if(pat!=None):
        return render(request, 'mediaid/patprofile.html',{'pat':pat})
    else:
        return render(request, 'mediaid/patprofile.html')










@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def updatedoc(request, id):
    if request.method == 'POST':
        try:
            dl = Doctor.objects.get(id=id)
            fm = DoctorUpdateForm(request.POST, request.FILES, instance=dl)
            if fm.is_valid():
                fm.save()
                return redirect('docprofile')
        except:
            messages.warning(request,"sorry, could not update doctor information!!")
            return render(request, 'mediaid/docprofile.html',{'message':messages})
    else:
        dl = Doctor.objects.get(id=id)
        fm = DoctorUpdateForm(instance=dl)
    return render(request, 'mediaid/updatedoc.html', {'form':fm})











@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def updatepat(request, id):
    if request.method == 'POST':
        try:
            dl = Patient.objects.get(id=id)
            fm = PatientUpdateForm(request.POST, request.FILES, instance=dl)
            ins = InsuranceProvider.objects.all()
            if fm.is_valid():
                insurance = fm.cleaned_data['insurance']
                insp = InsuranceProvider.objects.filter(id__icontains=insurance)
                if(insp):
                    fm.save()
                    return redirect('patprofile')                     
                else:
                    messages.warning(request,"Enter valid Insurance company id!!")
                    return render(request, 'mediaid/updatepat.html',{'message':messages, 'form':fm, 'ins':ins})
        except:
            messages.warning(request,"sorry, could not update patient information!!")
            return render(request, 'mediaid/patprofile.html',{'message':messages})
    else:
        ins = InsuranceProvider.objects.all()
        dl = Patient.objects.get(id=id)
        fm = PatientUpdateForm(instance=dl)
    return render(request, 'mediaid/updatepat.html', {'form':fm, 'ins':ins})










@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def confirm_pat_del(request, id):
            dl = Patient.objects.get(id=id)
            return render(request, 'mediaid/confirm_pat_del.html',{'pat':dl})










@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def del_patient(request, id):
    if request.method == 'POST':
        try:
            dl = Patient.objects.get(id=id)
            dl.delete()
            messages.success(request,"successfully deleted patient profile!!")
            return render(request, 'mediaid/patprofile.html',{'message':messages})
        except:
            messages.warning(request,"could not delete patient profile!!")
            return render(request, 'mediaid/patprofile.html',{'message':messages, 'pat':dl})
        










@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def confirm_doc_del(request, id):
            dl = Doctor.objects.get(id=id)
            return render(request, 'mediaid/confirm_doc_del.html',{'doc':dl})









@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def del_doctor(request, id):
    if request.method == 'POST':
        try:
            dl = Doctor.objects.get(id=id)
            dl.delete()
            messages.success(request,"successfully deleted doctor profile!!")
            return render(request, 'mediaid/docprofile.html',{'message':messages})
        except:
            messages.warning(request,"could not delete doctor profile!!")
            return render(request, 'mediaid/docprofile.html',{'message':messages, 'doc':dl})








@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def mydoctors(request):
    usr = request.user
    try:
        pat = Patient.objects.get(users_id=usr.id)
    except:
        messages.warning(request,"First register as a patient")
        return render(request, 'mediaid/mydoctors.html')
    try:
        app = Appointment.objects.filter(patient=pat)
    except:
        app = None
    if(app!=None):
        doc = []
        try:
            for a in app:
                doc = Doctor.objects.filter(id= a.doctor.id)
        except:
            doc = None
    if(doc!=None):
        return render(request, 'mediaid/mydoctors.html',{'doc':doc})
    else:
        return render(request, 'mediaid/mydoctors.html')
       



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def mypatients(request):
    usr = request.user
    try:
        doc = Doctor.objects.get(users_id=usr.id)
    except:
        messages.warning(request,"First register as a doctor")
        return render(request, 'mediaid/mypatients.html')
    try:
        app = Appointment.objects.filter(doctor=doc)
    except:
        app = None
    if(app!=None):
        pat = []
        try:
            for a in app:
                pat = Patient.objects.filter(id= a.patient.id)
        except:
            pat = None
    if(pat!=None):
        return render(request, 'mediaid/mypatients.html',{'pat':pat})
    else:
        return render(request, 'mediaid/mypatients.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def healthhistory(request):
    return render(request, 'mediaid/healthhistory.html')









# def receivedMessages(request, id):
#     user = request.user
#     try:
#         dfrnd = Friend.objects.get(doctor_id = id)
#     except:
#         dfrnd = None
#     try:
#         pfrnd = Friend.objects.get(patient_id = id)
#     except:
#         pfrnd = None
#     arr = []
#     if(dfrnd!=None):
#         chats = ChatMessage.objects.filter(msg_sender=user.username, msg_receiver=dfrnd.doctor.name)
#         for chat in chats:
#             arr.append(chat.body)
#         return JsonResponse(arr, safe=False)
#     elif(pfrnd!=None):
#         chats = ChatMessage.objects.filter(msg_sender=user.username, msg_receiver=pfrnd.patient.name)
#         for chat in chats:
#             arr.append(chat.body)
#         return JsonResponse(arr, safe=False)




# def chatNotification(request):
#     user = request.user.profile
#     friends = user.friends.all()
#     arr = []
#     for friend in friends:
#         chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
#         arr.append(chats.count())
#     return JsonResponse(arr, safe=False)
    





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def chatbot(request):
    usr = request.user
    chatbot_response = None  # Initialize chatbot_response variable
    user_input = None  # Initialize user_input variable

    if request.method == 'POST':
        user_input = request.POST.get('userMessage')
        prompt = user_input

        try:
            # Make the API request to OpenAI
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=256,
                temperature=0.5,
            )

            # Check the HTTP status code in the response
            if response.status_code == 200:
                chatbot_response = response.choices[0].text  # Store chatbot response

        except Exception as e:
            # Handle any exceptions that may occur during the API request
            error_message = f"An error occurred: {str(e)}"
            return render(request, 'mediaid/chat.html', {
                'usr': usr,
                'error_message': error_message,
                'active': 'btn-info'
            })

    # Render the chat.html template with chatbot_response and user_input
    return render(request, 'mediaid/chat.html', {
        'usr': usr,
        'response': chatbot_response,
        'user_input': user_input,
        'active': 'btn-info'
    })

# def chatbot(request):
#     usr = request.user
#     if api_key is not None and request.method == 'POST':
#         user_input = request.POST.get('userMessage')
#         prompt = user_input
#         response = openai.Completion.create(
#             engine = 'text-davinci-003',
#             prompt = prompt,
#             max_tokens = 256,
#             temperature = 0.5,
#         )
#         print(response)
#         chatbot_response = response["choices"][0]["text"]
#         return render(request, 'mediaid/chat.html',{'usr':usr,'response':chatbot_response, 'user_input':user_input,'active':'btn-info'})
#     else:
#         return render(request, 'mediaid/chat.html',{'usr':usr,'active':'btn-info'})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def prescription(request):
    usr = request.user
    try:
        doc = Doctor.objects.get(users_id=usr.id)
    except:
        doc = None
    try:
        pat = Patient.objects.get(users_id=usr.id)
    except:
        pat = None
    if(doc!=None):
        try:
            appd = Prescription.objects.filter(doctor= doc)
        except:
            appd = None
    else:
        appd = None
    if(pat!=None):
        try:
            appp = Prescription.objects.filter(patient= pat)
        except:
            appp = None
    else:
        appp = None
    if(appd!=None):
        if(appp!=None):
            return render(request, 'mediaid/prescription.html',{'appd':appd,'appp':appp})
        else:
            return render(request, 'mediaid/prescription.html',{'appd':appd})
    else:
        if(appp!=None):
            return render(request, 'mediaid/prescription.html',{'appp':appp})
        else:
            return render(request, 'mediaid/prescription.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def patprescription(request,id):
    try:
        pres = Prescription.objects.get(id=id)
    except Prescription.DoesNotExist:
        pres = None
    if(pres!=None):
        return render(request, 'mediaid/patprescription.html',{'pres':pres})
    else:
        return render(request, 'mediaid/patprescription.html',{'pres':pres})






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def doctorsprofile(request, id):
    try:
        doc = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        doc = None
    if(doc!=None):
        return render(request, 'mediaid/doctorsprofile.html',{'doc':doc})
    else:
        return render(request, 'mediaid/doctorsprofile.html',{'doc':doc})








@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def patientprofile(request, id):
    try:
        pat = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        doc = None
    if(pat!=None):
        return render(request, 'mediaid/patientprofile.html',{'pat':pat})
    else:
        return render(request, 'mediaid/patientprofile.html',{'pat':pat})







def img_to_txt(img, id):
    image_text = pytesseract.image_to_string(Image.open("media/"+img))
    text = image_text
    try:
        pr = Prescription.objects.get(id=id)
        pr.presctext = text
        pr.save()
    except Prescription.DoesNotExist:
        print("Could Not save")





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def indivprescription(request, id):
    usr = request.user
    try:
        pat = Patient.objects.get(id=id)
    except:
        pat = None
    if(pat!=None):
        try:
            appd = Prescription.objects.filter(patient= pat)
        except:
            appd = None
    else:
        appd = None
    if(pat!=None):
        if(appd!=None):
            return render(request, 'mediaid/indivpres.html',{'appd':appd})
        else:
            return render(request, 'mediaid/indivpres.html')
    else:
        return render(request, 'mediaid/idivpres.html')

# Insurance Serializer
class InsuranceList(ListAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceSerializer

class CreateInsuranceAPI(CreateAPIView):
    serializer_class = InsuranceSerializer

class InsuranceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceSerializer
    lookup_field = 'pk'

# Doctor API
class DoctorList(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class CreateDoctorAPI(CreateAPIView):
    serializer_class = DoctorSerializer

class DoctorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = 'pk'




# Patient API
class PatientList(ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class CreatePatientAPI(CreateAPIView):
    serializer_class = PatientSerializer

class PatientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'pk'


#Prescription API
class PrescriptionList(ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class CreatePrescriptionAPI(CreateAPIView):
    serializer_class = PrescriptionSerializer

class PrescriptionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    lookup_field = 'pk'


#Appointment API
class AppointmentList(ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class CreateAppointmentAPI(CreateAPIView):
    serializer_class = AppointmentSerializer

class AppointmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = 'pk'

#Comission API
class ComissionList(ListAPIView):
    queryset = Comission.objects.all()
    serializer_class = ComissionSerializer

class CreateComissionAPI(CreateAPIView):
    serializer_class = ComissionSerializer

class ComissionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comission.objects.all()
    serializer_class = ComissionSerializer
    lookup_field = 'doctor'

    def get_object(self):
        # Customize the behavior to retrieve the object by the 'doctor' field
        doctor_value = self.kwargs.get(self.lookup_field)
        obj = self.queryset.filter(doctor=doctor_value).first()
        if obj is None:
            # Handle the case where the object is not found
            raise Http404("Comission does not exist for the specified doctor.")
        return obj


class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter