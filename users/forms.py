from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput)



    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture']

