# from .models import Appointment, Doctor
# from django.views.decorators.cache import cache_control
# from django.contrib.auth.decorators import login_required

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required
# def get_notification(request):
#     if request.user.is_authenticated():
#         usr = request.user
#         try:
#             doc = Doctor.objects.get(users_id=usr.id)
#         except:
#             doc = None
#         if(doc!=None):
#             try:
#                 count = (Appointment.objects.filter(accepted=False)  & Appointment.objects.filter(doctor=doc)).count()
#             except:
#                 count = None
#         data = {
#             "count": count
#         }
#         return data
#     else:
#         count = None
#         data = {
#             "count": count
#         }
#         return data
