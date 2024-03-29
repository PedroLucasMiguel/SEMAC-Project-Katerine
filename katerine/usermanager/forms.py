from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .semac_utils import *
from .models import SemacUser


class SemacUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SemacUserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'nes-input is-dark semac-field', 'id': 'email'})
        self.fields['username'].label = 'E-mail'
        self.fields['password'].widget.attrs.update({'class': 'nes-input is-dark semac-field', 'id': 'password'})

    class Meta:
        model = SemacUser
        fields = ('username', 'password')


class SemacUserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SemacUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'nes-input is-dark semac-field', 'id': 'email'})
        self.fields['password1'].widget.attrs.update({'class': 'nes-input is-dark semac-field', 'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'class': 'nes-input is-dark semac-field', 'id': 'password'})

    class Meta:
        model = SemacUser
        fields = ('email', 'password1', 'password2')


class EmailAuthenticationForm(forms.Form):
    code = forms.CharField(
        label='Código de autenticação',
        max_length=FieldMaxLength.AUTHENTICATION_CODE,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'authentication-code-field',
            }
        )
    )


class PersonalDataForm(forms.Form):

    full_name = forms.CharField(
        label='Nome Completo',
        max_length=FieldMaxLength.FULL_NAME,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'full-name-field',
                'placeholder': 'Dawn S. Pearl'
            }
        )
    )

    cpf = forms.CharField(
        label='CPF',
        max_length=FieldMaxLength.CPF,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
                'id': 'state-field',
            }
        )
    )

    city = forms.CharField(
        label='Cidade',
        max_length=FieldMaxLength.CITY,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
                'id': 'contact-number-field'
            }
        )
    )

    class Meta:
        fields = ('full_name', 'cpf', 'dob', 'state', 'city', 'address', 'contact_number')


class PersonalDataUnespForm(forms.Form):

    full_name = forms.CharField(
        label='Nome Completo',
        max_length=FieldMaxLength.FULL_NAME,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
                'id': 'cpf-field',
                'placeholder': '000.000.000-00'
            }
        )
    )

    ra = forms.CharField(
        label='RA',
        max_length=FieldMaxLength.RA,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'ra-field',
                'placeholder': '00000000'
            }
        )
    )

    course_name = forms.CharField(
        label='Nome do curso',
        max_length=FieldMaxLength.COURSE_NAME,
        required=True,
        widget=forms.Select(
            choices=IbilceCourses.courses,
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'course-name-field'
            }
        )
    )

    dob = forms.DateTimeField(
        label='Data de nascimento',
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
                'id': 'state-field',
            }
        )
    )

    city = forms.CharField(
        label='Cidade',
        max_length=FieldMaxLength.CITY,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
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
                'class': 'nes-input is-dark semac-field',
                'id': 'contact-number-field'
            }
        )
    )

    class Meta:
        fields = ('full_name', 'cpf', 'dob', 'state', 'city', 'address', 'contact_number')


class PaymentConfirmationForm(forms.Form):
    image = forms.ImageField(
        label='Comprovante de pagamento',
        required=False,
    )

    class Meta:
        fields = ('image',)


class SubscriptionConfirmationForm(forms.Form):

    cpf = forms.CharField(
        label='CPF',
        max_length=FieldMaxLength.CPF,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'cpf-field',
                'placeholder': '000.000.000-00'
            }
        )
    )

    subscription_type = forms.CharField(
        label='Tipo de inscrição',
        max_length=FieldMaxLength.SUBSCRIPTION_TYPE,
        required=True,
        widget=forms.Select(
            choices=Subscriptions.types,
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'course-name-field'
            }
        )
    )


class ResetPasswordSendCodeForm(forms.Form):

    email = forms.EmailField(
        label='Email da conta',
        max_length=FieldMaxLength.EMAIL,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'email-field'
            }
        )
    )


class ResetPasswordWithCodeForm(forms.Form):

    email = forms.EmailField(
        label='Email da conta',
        max_length=FieldMaxLength.EMAIL,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'email-field'
            }
        )
    )

    code = forms.CharField(
        label='Código',
        max_length=FieldMaxLength.AUTHENTICATION_CODE,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'email-field'
            }
        )
    )

    password1 = forms.CharField(
        label='Nova senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'password1'
            }
        )
    )

    password2 = forms.CharField(
        label='Confirme nova senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'nes-input is-dark semac-field',
                'id': 'password2'
            }
        )
    )

    def clean_and_verify_password(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 != p2:
            raise PasswordNotEqualException('Passwords are not equal')

        if len(p1) < 8:
            raise SmallPasswordException('Small password')

        return p1

