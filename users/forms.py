from django import forms
from .models import Profile
from .widgets import DatePickerInput


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput)
    birth_date = forms.DateField(widget=DatePickerInput)



    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture', 'comes_from',
                  'birth_date', 'about_me', 'gender', 'mobile', 'email_visibility',
                  'mobile_visibility']

