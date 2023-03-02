from allauth.account.forms import SignupForm, LoginForm
from django import forms
from . import models


class MyCustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)


class MyCustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}), required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}), required=True)
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(
        attrs={'placeholder': '+353 XX XXX XXXX'}), required=False)
    dob = forms.DateField(label=('DOB'), widget=forms.DateInput(
        format=('%d/%m/%Y'), attrs={'type': 'date'}), required=True)
    photo = forms.ImageField(label='Photo', required=False)

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.dob = self.cleaned_data['dob']
        user.photo = self.cleaned_data['photo']
        user.save()
        return user


class MyCustomUserForm(forms.ModelForm):

    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'phone', 'dob', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Last Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': '0XX XXX XXXX',
            }),
            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Date of Birth',
            })}
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone',
            'dob': 'DOB',
        }


class MyFamilioForm(forms.ModelForm):

    class Meta:
        model = models.Familio
        fields = ['email', 'name', 'level', 'kinship']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email',
            }),
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
            'level': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Level',
            }),
            'kinship': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Kinship',
            })}
        labels = {
            'email': 'Email Address',
            'name': 'Full Name',
            'level': 'Member Level',
            'kinship': 'Kinship',
        }


class MyGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        my_familio = kwargs.pop('my_familio')
        super().__init__(*args, **kwargs)
        self.fields['familio'].queryset = models.Familio.objects.filter(
            member=my_familio)

    class Meta:
        model = models.Group
        fields = ['grp_name', 'familio']
        widgets = {
            'grp_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Group Name',
            }),
            'familio': forms.SelectMultiple(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Familio Members'
            })}
        labels = {
            'grp_name': 'Group Name',
            'familio': 'Familio Members'
        }
