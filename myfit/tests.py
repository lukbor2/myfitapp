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
        #Step 1: before writing any activity to the db, I need to setup a user, a device owner and a device; otherwise I can not write an activity to the db.
        new_user = User.objects.create_user('test for test', 'test_for_test@gmail.com', 'test_for_testpassword')
        new_user.save() #Because of the signal sent to the Device_Owner model, a Device_Owner instance is created at this point. But it does not have any field filled with data.

        new_device_owner = Device_Owner.objects.get(user = new_user) #Here I retrieve the Device_Owner instance just created by the function called with the signal from the post_save in User.
        #Then I fill the fields for the Device_Owner instance and then save it to the db.
        new_device_owner.name = 'test'
        new_device_owner.surname = 'for test'
        new_device_owner.date_of_birth = '1971-03-31'
        new_device_owner.age = 47
        new_device_owner.sex = 'M'
        new_device_owner.heart_rate_rest = 55
        new_device_owner.save()

        new_device = Device(device_serial_no = 'ECF0325109001300', device_model = 'device_model_test', device_name = 'device_name_test', device_owner = new_device_owner)
        new_device.save()

        #End of Step 1.
        #Step 2: write some activities to the db. The activities are in a pre-defined folder.
        test_folder = '/home/luca/git/myfitapp/Logs_Test' #I assume this is a folder where I have the files I want to test.
        p = Path(test_folder)
        error_message = create_activity_from_file(p) #Using the function I wrote in the view to write to the db. This is the function I want to test.
        print(error_message)
        self.activities = Activity.objects.all()
        print('There are ', len(self.activities), ' activities in the db to test.')
        print('End of the Setup.')

        #End of Step 2.

        #Step 3: prepare the expected values. I will test the values written in the db with the values I have here. And I read them from a file.
        def build_test_values(test_results):
            f = open(test_results)
            results = []
            l = f.readline()
            while l != '':
                l = l.strip('\n')
                l = l.replace(' ', '')
                l = l.split(',') #Now I have a list....
                results.append(l)
                l = f.readline()

            return results

        test_results = '/home/luca/git/myfitapp/test_data.txt' #This is a pre-defined file with the expected results of the tests.
        self.results = build_test_values(test_results)

    #TODO: The next two tests are ok, but I have to do something like this for every field I am testing (so if the test fails I know which field caused the problem).
    #TODO: see if/how to use subTest to avoid writing one test for each field. I started below but I did not finish.
    def test_activity_time_original(self):
        for a in self.activities:
            for res_line in self.results:
                if res_line[0] == a.activity_id: #Found the line corresponding to the activitiy I am looking at.
                    print('Testing activity ', res_line[0], ' for activity_time_original...')
                    self.assertEqual(a.activity_time_original, res_line[1])
                    break

    def test_activity_duration(self):
        for a in self.activities:
            for res_line in self.results:
                if res_line[0] == a.activity_id: #Found the line corresponding to the activitiy I am looking at.
                    print('Testing activity ', res_line[0], ' for activity_duration...')
                    self.assertEqual(a.activity_duration, int(res_line[2]))
                    break

    def test_activity_in_db(self):
        for a in self.activities:
            for res_line in self.results:
                if res_line[0] == a.activity_id: #Found the line corresponding to the activitiy I am looking at.
                    print('Testing activity ', res_line[0])
                    with self.subTest():
