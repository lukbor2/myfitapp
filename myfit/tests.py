from django.test import TestCase
from myfit.models import Activity, Device_Owner, Device
import xml.etree.ElementTree as ET
from pathlib import Path
from decimal import Decimal
from datetime import datetime

# Create your tests here.

class ActivityLoadTestCase(TestCase):
    """
    Load some pre-defined test files and checking the data are what I expect.
    """
    def setUp(self):
        test_folder = '/home/luca/git/myfitapp/Logs_Test' #I assume this is a folder where I have the files I want to test.
        p = Path(test_folder)
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

    #THIS TEST DOES NOT MAKE SENSE. I HAVE TO CHANGE THE ACTIVITY MODEL OR THE VIEW TO HAVE A FUNCTION WHICH DOES THE JOB OF SETTING THE DATA AND THEN TEST THAT FUNCTION.
    def test_activity_device_used(self):
        activities = Activity.objects.all()
        for a in activities:
            self.assertEqual(a.activity_device_used, 'ECF0325109001300')
