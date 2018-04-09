from django.forms import ModelForm
from myfit.models import Device_Owner

class ProfileForm(ModelForm):
    class Meta:
        model = Device_Owner
        fields = ['name', 'surname', 'date_of_birth', 'sex', 'height', 'weight', 'heart_rate_rest',]
