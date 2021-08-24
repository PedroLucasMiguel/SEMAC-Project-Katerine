from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from .semac_utils import *
from .models import SemacUser


class SemacUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SemacUserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': '#', 'id': 'email'})
        self.fields['password'].widget.attrs.update({'class': '#', 'id': 'password'})

    class Meta:
        model = SemacUser
        fields = ('username', 'password')


class SemacUserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SemacUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': '#', 'id': 'email'})
        self.fields['password1'].widget.attrs.update({'class': '#', 'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'class': '#', 'id': 'password'})

    class Meta:
        model = SemacUser
        fields = ('email', 'password1', 'password2')


class PersonalDataForm(forms.Form):

    full_name = forms.CharField(
        label='Nome Completo',
        max_length=FieldMaxLength.FULL_NAME,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark',
                'id': 'full-name-field',
                'placeholder': 'Dawn Pearl'
            }
        )
    )

    cpf = forms.CharField(
        label='CPF',
        max_length=FieldMaxLength.CPF,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark',
                'id': 'cpf-field',
                'placeholder': '000.000.000-00'
            }
        )
    )

    dob = forms.DateTimeField(
        label='Data de nascimento',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'nes-input is-dark',
                'id': 'dob-field',
                'type': 'date',
            }
        )
    )

    state = forms.CharField(
        label='Estado',
        max_length=FieldMaxLength.STATE,
        required=True,
        widget=forms.Select(
            choices=BrazilStates.states,
            attrs={
                'class': 'nes-input is-dark',
                'id': 'state-field',
                'placeholder': '000.000.000-00'
            }
        )
    )

    city = forms.CharField(
        label='Cidade',
        max_length=FieldMaxLength.CITY,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark',
                'id': 'city-field',
            }
        )
    )

    address = forms.CharField(
        label='Endereço',
        max_length=FieldMaxLength.ADDRESS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark',
                'id': 'address-field'
            }
        )
    )

    contact_number = forms.CharField(
        label='Telefone de contato',
        max_length=FieldMaxLength.CONTACT_NUMBER,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark',
                'id': 'contact-number-field'
            }
        )
    )

    class Meta:
        fields = ('full_name', 'cpf', 'dob', 'state', 'city', 'address', 'contact_number')


class PersonalDataUnespForm(forms.Form):

    full_name = forms.CharField(
        max_length=FieldMaxLength.FULL_NAME,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': '#',
                'id': 'full-name-field',
                'placeholder': 'Dawn Pearl'
            }
        )
    )

    cpf = forms.CharField(
        max_length=FieldMaxLength.CPF,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': '#',
                'id': 'cpf-field',
                'placeholder': '000.000.000-00'
            }
        )
    )

    ra = forms.CharField(
        max_length=FieldMaxLength.RA,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': '#',
                'id': 'ra-field',
                'placeholder': '00000000'
            }
        )
    )

    course_name = forms.CharField(
        max_length=FieldMaxLength.COURSE_NAME,
        required=True,
        widget=forms.Select(
            choices=IbilceCourses.courses,
            attrs={
                'class': '#',
                'id': 'course-name-field'
            }
        )
    )

    dob = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'class': '#',
                'id': 'dob-field',
            }
        )
    )

    state = forms.CharField(
        max_length=FieldMaxLength.STATE,
        required=True,
        widget=forms.Select(
            choices=BrazilStates.states,
            attrs={
                'class': '#',
                'id': 'state-field',
                'placeholder': '000.000.000-00'
            }
        )
    )

    city = forms.CharField(
        max_length=FieldMaxLength.CITY,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': '#',
                'id': 'city-field',
            }
        )
    )

    address = forms.CharField(
        max_length=FieldMaxLength.ADDRESS,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': '#',
                'id': 'address-field'
            }
        )
    )

    contact_number = forms.CharField(
        max_length=FieldMaxLength.CONTACT_NUMBER,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': '#',
                'id': 'contact-number-field'
            }
        )
    )

    class Meta:
        fields = ('full_name', 'cpf', 'dob', 'state', 'city', 'address', 'contact_number')

