from django.shortcuts import render, redirect
from django.views import generic
from myfit.models import Activity, Device_Owner, Device
from django.db import transaction
from django.contrib.auth import login, authenticate
from myfit.forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import xml.etree.ElementTree as ET
import math
from pathlib import Path
from decimal import Decimal
from datetime import datetime

def home(request):
    return render(request, 'myfit/home.html')

class ActivityListView(generic.ListView):
    model = Activity

    #filtering the activities based on the user connected to the device used for the activity.
    def get_queryset(self):
        return Activity.objects.filter(activity_device_used__device_owner__user = self.request.user)

class ActivityDetailView(generic.DetailView):
    model = Activity

@transaction.atomic
def create_user_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = ProfileForm(request.POST, instance=user.device_owner)  # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()  # Gracefully save the form
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'myfit/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
})

class ProfileUpdateView(generic.UpdateView):
        model = Device_Owner
        form_class = ProfileForm
        #As I am specifying a form_class based on the form model I created, I don't need to list the fields here. I thought it make sense to use the same form model I used for signup.
        #fields = ['name', 'surname', 'date_of_birth', 'sex', 'height', 'weight', 'heart_rate_rest']

        def get_success_url(self):
            return reverse_lazy('myfit-activities')

def upload_activities_view(request):
    #Using this view to upload the activities from a given folder. Each activity is a .log file.
    #The folder in defined in the user's profile.

    logs_folder = str(request.user.device_owner.log_files_location)
    p = Path(logs_folder)
    for file in p.iterdir():
        tree = ET.parse(file)
        root = tree.getroot()
        a_id = root[2].text

        a_time_original = root[1].text
        date_and_time = a_time_original.split('T') #This is a list with the date as first element and time as the second one.
        a_date = datetime.strptime(date_and_time[0], '%Y-%m-%d')
        a_time = datetime.strptime(date_and_time[1], '%H:%M:%S')

        a_duration = int(root[5][0][1].text)
        a_speed_avg = Decimal(float(root[5][0][7][0].text)/1000)
        a_speed_max = Decimal(float(root[5][0][7][1].text)/1000)
        a_hr_avg = int(root[5][0][10][0].text)
        a_hr_max = int(root[5][0][10][1].text)
        a_hr_min = int(root[5][0][10][2].text)
        a_type = int(root[5][0][12].text)
        a_type_name = root[5][0][13].text
        a_device_used = Device.objects.get(pk=root[0].text)

        a_hh, a_mm, a_ss = calculate_duration(a_duration)

        new_activity = Activity(activity_id = a_id, activity_time_original = a_time_original, activity_date = a_date ,activity_time = a_time , activity_duration = a_duration, activity_speed_avg = a_speed_avg,
        activity_speed_max = a_speed_max, activity_hr_avg = a_hr_avg, activity_hr_max = a_hr_max, activity_hr_min = a_hr_min, activity_type = a_type,
        activity_type_name = a_type_name, activity_device_used = a_device_used, activity_duration_hh = a_hh, activity_duration_mm = a_mm, activity_duration_ss = a_ss)

        #By default Django will execute an update when a log file related to an existing activity is read. This is the default behavior.
        new_activity.save()

    return render(request, 'myfit/upload_activities.html', {'logs_folder': logs_folder})

def calculate_duration(original):
    #Transforms the numeber coming from the log files representing the duration into hours, minutes and seconds.

    x = original / 1000
    y = x / 3600
    if y > 1:
        a, b = math,modf(y)
        hh = int(b)
    else:
        hh = 0

    z = y - hh
    y = z * 60

    if y > 1:
        a, b = math.modf(y)
        mm = int(b)
    else:
        mm = 0

    z = y - mm
    y = z * 60
    ss = int(y)

    return (hh, mm, ss)
