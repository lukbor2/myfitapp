from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/', views.home, name='myfit-home'),
    path('signup/', views.create_user_view , name='myfit-signup'),
    path('activities/', login_required(views.ActivityListView.as_view()), name='myfit-activities'), #As I am using a class-based view I need to put the decorator here.
    path('upload_activities/', login_required(views.upload_activities_view), name='myfit-upload-activities'), 
    re_path(r'activity/(?P<pk>[-\w]+)/$', login_required(views.ActivityDetailView.as_view()), name='activity-detail'),
    re_path(r'device_owner/(?P<pk>[-\w]+)/$', login_required(views.ProfileUpdateView.as_view()) , name='owner-detail'),
    path('accounts/', include('django.contrib.auth.urls')), # This is to include the default views available for authenticating users.
]
