from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/', views.home, name='myfit-home'),
    path('activities/', login_required(views.ActivityListView.as_view()), name='myfit-activities'), #As I am using a class-based view I need to put the decorator here.
    re_path(r'activity/(?P<pk>[-\w]+)/$', views.ActivityDetailView.as_view(), name='activity-detail'),
    path('accounts/', include('django.contrib.auth.urls')), # This is to include the default views available for authenticating users.
]
