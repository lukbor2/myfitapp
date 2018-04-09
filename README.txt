OBJECTIVE

Use OpenAmbit to download the data from the Suunto device.
OpenAmbit stores each activity in a .log file.
I want to read the log file, store the data in a database and then visualize / analyze the data with a webapp.

THE .LOG FILE

The .log file is an xml file.
I did not find any documentation about its structure, therefore I am "guessing" how it works.
For what I can see there are some header information about the activity.
Then a section delimited by <log></log> starts; this section has the detailed data, i.e. the "samples" taken by the device as the activity goes on.
I will have to use these data to have time-dependent measures, not just summarized measures (like average values).

Read here https://docs.python.org/3/library/xml.etree.elementtree.html to learn about how to handle xml in python.

THE UML MODEL

I am working on a UML model first. Then I will start building the Django models from there.

TODOs

- Complete the view where I upload the activities. IMPORTANT: how to handle log files which have been already loaded; decide what to do.
- Implement security, so that a device owner can see the data related to his device(s) only.
- Find and implement a formula to calculate the limits of all heart rate zones.
- Where do I implement the methods to set the "calculated fields of my models"? I think I have to do that in views not in the models.
  Look at models.py in bptrack; in there I implemented a method in the models.
- I should also think how to keep those calculated fields updated (e.g. the age changes once per year). It is not top priority.
- Add to the uml model and to the django app the remaining header data (i.e. those I have not included yet).
- Add the <log></log> data to the uml model and to the django app.
- Implement the device-detail view and update url.py
- Implement the activty-detail view and update url.py
- In activity_list.html work on the chart (there is a starting point and use Bootstrap Dashboard example)
- Find a way for the user to define a default folder where the logs are stored and a way to change it.
