from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse

from . import forms, models
from .semac_utils import *
from .semac_smtp import gmail_smtp_service_provider


def home_page(request):
    return render(request, 'Homepage.html', {})


def login_page(request):
    if request.POST:
        form = forms.SemacUserLoginForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('/profile/')

        return render(request, 'Login.html', {'form': form})

    if not request.user.is_authenticated:
        form = forms.SemacUserLoginForm()
        return render(request, 'Login.html', {'form': form})

    return redirect('/')


def logout_page(request):
    logout(request)
    return redirect('/')


def profile_page(request):
    if request.user.is_authenticated:

        if request.user.is_email_authenticated:
            try:
                personal_data = models.UserPersonalData.objects.get(user_email=request.user)
                lectures = models.PersonOnLecture.objects.filter(user_cpf=personal_data).all()
                return render(request, 'Profile.html', {'pd': personal_data, 'lc': lectures})

            except ObjectDoesNotExist:
                return redirect('/are-you-unesp/')

        return redirect('/authenticate-email/')

    return redirect('/login/')


def register_page(request):
    if request.POST:
        form = forms.SemacUserRegisterForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)  # Login necessário para criar informações pessoais
            return redirect('/authenticate-email/')

        return render(request, 'Register.html', {'form': form})

    form = forms.SemacUserRegisterForm()
    return render(request, 'Register.html', {'form': form})


def email_authentication(request):
    if request.user.is_authenticated:

        if not request.user.is_email_authenticated:

            if request.POST:
                code_on_db = models.SemacUserAuthenticationCode.objects.get(user_email=request.user)
                code = code_on_db.code
                form = forms.EmailAuthenticationForm(data=request.POST)

                if form.is_valid():
                    code_form = form.cleaned_data['code'].upper()
                    if code_form == code:
                        request.user.is_email_authenticated = True
                        request.user.save()
                        code_on_db.delete()
                        return redirect('/are-you-unesp/')
                    else:
                        messages.error(request, 'Código informado não é valido!')

                return render(request, 'EmailAuthenticationPage.html', {'form': form})

            if not models.SemacUserAuthenticationCode.objects.filter(user_email=request.user).exists():
                code = gmail_smtp_service_provider.send_verification_code(request.user.email)
                semac_user_authentication_code = models.SemacUserAuthenticationCode(
                    code=code,
                    user_email=request.user
                )
                semac_user_authentication_code.save()

            form = forms.EmailAuthenticationForm()
            return render(request, 'EmailAuthenticationPage.html', {'form': form})

        return redirect('/')

    return redirect('/login/')


def are_you_unesp_page(request):
    if request.user.is_authenticated:

        if not models.UserPersonalData.objects.filter(user_email=request.user).exists():
            return render(request, 'AreYouUnesp.html', {})

        return redirect('/')

    return redirect('/login/')


def personal_data_page(request):
    if request.POST:
        form = forms.PersonalDataForm(data=request.POST)

        if form.is_valid():
            '''
            Uma dica para gerações futuras, tentem melhorar o que foi feito nesta parte.
            O método usado aqui de fato funciona, mas definitivamente não é o método mais elegante para fazer isso.
            '''
            try:
                full_name = Validators.full_name_validator(form.cleaned_data.get('full_name'))
                cpf = Validators.cpf_validator(form.cleaned_data.get('cpf'))
                dob = Validators.age_validator(form.cleaned_data.get('dob'), 11)
                state = form.cleaned_data.get('state')  # Não precisa pois a entrada ja é tratada por padrão
                city = Validators.city_validator(form.cleaned_data.get('city'))
                address = Validators.address_validator(form.cleaned_data.get('address'))
                contact_number = Validators.contact_number_validator(form.cleaned_data.get('contact_number'))

                if not models.UserPersonalData.objects.filter(cpf=cpf).exists():
                    personal_data = models.UserPersonalData(
                        full_name=full_name,
                        cpf=cpf,
                        user_email=request.user,
                        dob=dob,
                        state=state,
                        city=city,
                        address=address,
                        contact_number=contact_number,
                    )
                    personal_data.save()
                    return redirect('/profile/')

                messages.error(request, 'CPF Informado ja se encontra cadastrado')

            except FullNameNotValidException:
                messages.error(request, 'Nome informado inválido')

            except CpfNotValidException:
                messages.error(request, 'CPF informado inválido')

            except AgeNotValidException:
                messages.error(request, 'Idade informada inválido')

            except CityNotValidException:
                messages.error(request, 'Cidade informada inválido')

            except AddressNotValidException:
                messages.error(request, 'Endereço informado inválido')

            except ContactNumberNotValidException:
                messages.error(request, 'Telefone de contado informado inválido')

        return render(request, 'PersonalDataForm.html', {'form': form})

    if request.user.is_authenticated:

        if not models.UserPersonalData.objects.filter(user_email=request.user).exists():
            form = forms.PersonalDataForm()
            return render(request, 'PersonalDataForm.html', {'form': form})

        return redirect('/')

    return redirect('/login/')


def personal_data_unesp_page(request):
    if request.POST:
        form = forms.PersonalDataUnespForm(data=request.POST)

        if form.is_valid():
            '''
            Mesma coisa de antes...
            Só.... NÃO! (Predo agonizando por estar programando a 8 horas sem parar)
            (Se vocês não passaram por isso vcs não sabem oq é programar)
            
            (Pq eu escolhi comp mesmo?)
            '''
            try:
                full_name = Validators.full_name_validator(form.cleaned_data.get('full_name'))
                cpf = Validators.cpf_validator(form.cleaned_data.get('cpf'))
                ra = Validators.ra_validator(form.cleaned_data.get('ra'))
                course_name = form.cleaned_data.get('course_name')  # Não precisa de validação
                dob = Validators.age_validator(form.cleaned_data.get('dob'), 16)
                state = form.cleaned_data.get('state') # Não precisa de validação
                city = Validators.city_validator(form.cleaned_data.get('city'))
                address = Validators.address_validator(form.cleaned_data.get('address'))
                contact_number = Validators.contact_number_validator(form.cleaned_data.get('contact_number'))

                if not models.UserPersonalData.objects.filter(cpf=cpf).exists():
                    personal_data = models.UserPersonalData(
                        full_name=full_name,
                        cpf=cpf,
                        user_email=request.user,
                        dob=dob,
                        state=state,
                        city=city,
                        address=address,
                        contact_number=contact_number,
                    )

                    if not models.UserUnespData.objects.filter(ra=ra).exists():
                        personal_unesp_data = models.UserUnespData(
                            ra=ra,
                            course_name=course_name,
                            user_cpf=personal_data,
                        )
                        personal_data.save()
                        personal_unesp_data.save()
                        return redirect('/profile/')

                    else:
                        messages.error(request, 'RA informado já se encontra cadastrado no sistema')

                else:
                    messages.error(request, 'CPF Informado já se encontra cadastrado')

            except FullNameNotValidException:
                messages.error(request, 'Nome informado inválido')

            except CpfNotValidException:
                messages.error(request, 'CPF informado inválido')

            except AgeNotValidException:
                messages.error(request, 'Idade informada inválido')

            except CityNotValidException:
                messages.error(request, 'Cidade informada inválido')

            except AddressNotValidException:
                messages.error(request, 'Endereço informado inválido')

            except ContactNumberNotValidException:
                messages.error(request, 'Telefone de contado informado inválido')

            except RaNotValidException:
                messages.error(request, 'RA informado inválido')

        return render(request, 'PersonalDataForm.html', {'form': form})

    if request.user.is_authenticated:

        if not models.UserPersonalData.objects.filter(user_email=request.user).exists():
            form = forms.PersonalDataUnespForm()
            return render(request, 'PersonalDataForm.html', {'form': form})

        return redirect('/')

    return redirect('/login/')


def DEBUG_test_smtp(request):
    if request.user.is_authenticated:
        email = request.user.email
        gmail_smtp_service_provider.send_verification_code(email)
        return HttpResponse('Enviado?')
    return redirect('/')


def DEBUG_render_test(request):
    if request.POST:
        form = forms.SemacUserLoginForm(data=request.POST)
        if form.is_valid():
            answer = request.POST
            login(request, form.get_user())
            #form.save()
            return render(request, 'PersonalDataForm.html', {'form': form, 'answer': answer})
    answer = ['nada']
    form = forms.PersonalDataForm()
    return render(request, 'PersonalDataForm.html', {'form': form, 'answer': answer})


def DEBUG_testing_mesures(request):
    if request.user.is_authenticated:
        return render(request, 'TestingThreads.html', {'nome': request.user.email})
    return render(request, 'TestingThreads.html', {'nome': 'a'})

