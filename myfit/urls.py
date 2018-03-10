from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('home/', views.home, name='myfit-home'),
    path('activities/', views.ActivityListView.as_view(), name='myfit-activities'),
    re_path(r'activity/(?P<pk>[-\w]+)/$', views.ActivityDetailView.as_view(), name='activity-detail'),
    path('accounts/', include('django.contrib.auth.urls')), # This is to include the default views available for authenticating users.
]
