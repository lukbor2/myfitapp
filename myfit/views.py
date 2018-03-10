from django.shortcuts import render
from django.views import generic
from myfit.models import Activity, Device_Owner, Device

def home(request):
    return render(request, 'myfit/home.html')

class ActivityListView(generic.ListView):
    model = Activity

class ActivityDetailView(generic.DetailView):
    model = Activity
