from django.test import TestCase
from myfit.models import Activity, Device_Owner, Device
from myfit.views import create_activity_from_file
import xml.etree.ElementTree as ET
from django.contrib.auth.models import User
from pathlib import Path
from decimal import Decimal
from datetime import datetime

# Create your tests here.

class ActivityLoadTestCase(TestCase):
    """
    Load some pre-defined test files and checking the data are what I expect.
    """
    def setUp(self):
        new_user = User.objects.create_user('test for test', 'test_for_test@gmail.com', 'test_for_testpassword')
        new_user.save()
        new_user.refresh_from_db()  # This will load the Profile created by the Signal


        new_device_owner = Device_Owner(name = 'test', surname = 'for test', date_of_birth = '1971-03-31', age = 47, sex = 'M', heart_rate_rest = 55, instance=user.device_owner)
        #new_device_owner = Device_Owner(name = 'test', surname = 'for test', date_of_birth = '1971-03-31', age = 47, sex = 'M', heart_rate_rest = 55, user = new_user)
        new_device_owner.save()

        new_device = Device(device_serial_no = 'ECF0325109001300', device_model = 'device_model_test', device_name = 'device_name_test', device_owner = new_device_owner)
        new_device.save()

    def test_activity_device_used(self):
        test_folder = '/home/luca/git/myfitapp/Logs_Test' #I assume this is a folder where I have the files I want to test.
        p = Path(test_folder)
        error_message = create_activity_from_file(p)
        print(error_message)

        activities = Activity.objects.all()
        for a in activities:
            self.assertEqual(a.activity_device_used, 'ECF0325109001300')
