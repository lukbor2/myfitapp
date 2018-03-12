from django.shortcuts import render, redirect
from django.views import generic
from myfit.models import Activity, Device_Owner, Device
from django.db import transaction
from django.contrib.auth import login, authenticate
from myfit.forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'myfit/home.html')

class ActivityListView(generic.ListView):
    model = Activity
    # context_object_name = 'all_activities'

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
