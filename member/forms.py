from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser


class MyCustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}), required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}), required=True)
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(
        attrs={'placeholder': '+353 XX XXX XXXX'}), required=False)
    dob = forms.DateField(label=('DOB'), widget=forms.DateInput(format=('%d/%m/%Y'), attrs={
                          'class': 'form-control', 'type': 'date'}), required=True)
    photo = forms.ImageField(label='Photo', required=False)

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.dob = self.cleaned_data['dob']
        user.photo = self.cleaned_data['photo']
        user.save()
        return user
