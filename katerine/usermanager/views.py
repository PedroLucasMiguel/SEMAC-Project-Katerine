from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse

from . import forms, models
from .semac_utils import *
import datetime


def template_refresh_notifications(request):
    available_presences = []

    if request.user.is_authenticated:
        if hasattr(request.user, 'personal_data'):
            if models.Lecture.objects.filter(enable_presence_url=True).exists():
                lecture_query = models.Lecture.objects.filter(enable_presence_url=True).all()

                for lecture in lecture_query.iterator():
                    if not models.PersonOnLecture.objects.filter(lecture_id=lecture,
                                                                 user_cpf=request.user.personal_data).exists():
                        lecture_title = str(lecture.title)
                        lecture_link = lecture_title.replace(' ', '%20')
                        lecture_link = f'http://semac.cc/presence/{lecture_link}'
                        available_presences.append(lecture_link)

    return available_presences


def home_page(request):
    notifications = template_refresh_notifications(request)
    return render(request, 'Homepage.html', {'not': notifications})


def login_page(request):
    notifications = template_refresh_notifications(request)

    if request.POST:
        form = forms.SemacUserLoginForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('/profile/')

        return render(request, 'Login.html', {'form': form, 'not': notifications})

    if not request.user.is_authenticated:
        form = forms.SemacUserLoginForm()
        return render(request, 'Login.html', {'form': form, 'not': notifications})

    return redirect('/')


def logout_page(request):
    logout(request)
    return redirect('/')


def profile_page(request):
    notifications = template_refresh_notifications(request)

    if request.user.is_authenticated:

        if request.user.is_email_authenticated:
            try:
                personal_data = request.user.personal_data
                lectures = personal_data.participated_lectures.all()
                unesp_data = None
                sub_confirmation = None
                sub = None

                if hasattr(personal_data, 'unesp_data'):
                    unesp_data = personal_data.unesp_data

                if hasattr(personal_data, 'sub_confirmation'):
                    sub_confirmation = personal_data.sub_confirmation
                    if hasattr(personal_data, 'subscription'):
                        sub = personal_data.subscription

                return render(request, 'Profile.html', {
                    'pd': personal_data,
                    'lc': lectures,
                    'ud': unesp_data,
                    'sub_c': sub_confirmation,
                    'sub': sub,
                    'not': notifications,
                })

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

    if request.user.is_authenticated:
        return redirect('/')

    form = forms.SemacUserRegisterForm()
    return render(request, 'Register.html', {'form': form})


def email_authentication(request):
    if request.user.is_authenticated:

        if not request.user.is_email_authenticated:

            if request.POST:
                code_on_db = request.user.auth_code
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

            if not hasattr(request.user, 'auth_code'):
                code = generate_validation_code()
                write_to_smtp_queue(request.user.email, code)
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
            return render(request, 'AreYouUnesp.html')

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

                messages.error(request, 'CPF Informado já se encontra cadastrado!')

            except FullNameNotValidException:
                messages.error(request, 'Nome informado inválido!')

            except CpfNotValidException:
                messages.error(request, 'CPF informado inválido!')

            except AgeNotValidException:
                messages.error(request, 'Idade informada inválida! (Menor de 11 anos)')

            except CityNotValidException:
                messages.error(request, 'Cidade informada inválida!')

            except AddressNotValidException:
                messages.error(request, 'Endereço informado inválido!')

            except ContactNumberNotValidException:
                messages.error(request, 'Telefone de contado informado inválido!')

        return render(request, 'PersonalDataForm.html', {'form': form})

    if request.user.is_authenticated:

        if not hasattr(request.user, 'personal_data'):
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
                state = form.cleaned_data.get('state')  # Não precisa de validação
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
                        messages.error(request, 'RA informado já se encontra cadastrado no sistema!')

                else:
                    messages.error(request, 'CPF informado já se encontra cadastrado!')

            except FullNameNotValidException:
                messages.error(request, 'Nome informado inválido!')

            except CpfNotValidException:
                messages.error(request, 'CPF informado inválido!')

            except AgeNotValidException:
                messages.error(request, 'Idade informada inválida! (Menor de 16 anos)')

            except CityNotValidException:
                messages.error(request, 'Cidade informada inválida!')

            except AddressNotValidException:
                messages.error(request, 'Endereço informado inválido!')

            except ContactNumberNotValidException:
                messages.error(request, 'Telefone de contado informado inválido!')

            except RaNotValidException:
                messages.error(request, 'RA informado inválido!')

        return render(request, 'PersonalDataForm.html', {'form': form})

    if request.user.is_authenticated:

        if not hasattr(request.user, 'personal_data'):
            form = forms.PersonalDataUnespForm()
            return render(request, 'PersonalDataForm.html', {'form': form})

        return redirect('/')

    return redirect('/login/')


def presence_page(request, lecture_name='Abacaxi'):
    notifications = template_refresh_notifications(request)
    if request.user.is_authenticated:
        if hasattr(request.user, 'personal_data'):
            if models.Lecture.objects.filter(title=lecture_name).exists():
                lecture = models.Lecture.objects.get(title=lecture_name)
                personal_data = request.user.personal_data

                if lecture.enable_presence_url:
                    if hasattr(request.user.personal_data, 'subscription'):
                        if not models.PersonOnLecture.objects.filter(lecture_id=lecture, user_cpf=personal_data).exists():
                            person_on_lecture = models.PersonOnLecture(
                                lecture_id=lecture,
                                user_cpf=personal_data
                            )
                            person_on_lecture.save()

                            # É necessário realizar a atualização das notificações nesta etapa pois o usuário, após de fato
                            # O usuario adquirir a presença clicando no link, as notificações continuam mostrando a presença que
                            # ele ja pegou.
                            notifications = template_refresh_notifications(request)

                            return render(request, 'PresencePage.html', {'status': 'accounted', 'not': notifications})

                        return render(request, 'PresencePage.html', {'status': 'already_have', 'not': notifications})

                    else:
                        return render(request, 'PresencePage.html', {'status': 'no_subscription',
                                                                     'not': notifications})

                return render(request, 'PresencePage.html', {'status': 'not_enabled', 'not': notifications})

            return redirect('/')
        return redirect('/profile/')
    return redirect('/login/')


def buy_subscription_page(request):
    notifications = template_refresh_notifications(request)

    if request.user.is_authenticated and hasattr(request.user, 'personal_data'):
        form = forms.PaymentConfirmationForm()

        if not hasattr(request.user.personal_data, 'sub_confirmation'):
            if request.POST:

                form = forms.PaymentConfirmationForm(request.POST, request.FILES)

                if form.is_valid():
                    image = form.cleaned_data.get('image')

                    if image:
                        if image.size > 8 * 1024 * 1024:
                            messages.error(request, "Tamanho da imagem inválido ( > 8mb )")
                            return render(request, 'BuySubscriptionPage.html', {'form': form, 'not': notifications})

                        payment_confirmation = models.SubscriptionPaymentConfirmation(
                            user_cpf=request.user.personal_data,
                            payment_confirmation=image
                        )
                        payment_confirmation.save()

                        return render(request, 'PaymentConfirmationSended.html', {})

                    else:
                        messages.error(request, "Não foi possível ler a imagem enviada")

                return render(request, 'BuySubscriptionPage.html', {'form': form, 'not': notifications})

            return render(request, 'BuySubscriptionPage.html', {'form': form, 'not': notifications})

        messages.error(request, 'Nós já recebemos o seu comprovante!')
        return render(request, 'BuySubscriptionPage.html', {'form': form, 'not': notifications})

    return redirect('/login/')


def buy_subscription_page_placeholder(request):
    notifications = template_refresh_notifications(request)

    if request.user.is_authenticated:
        return render(request, 'BuySubscriptionPagePlaceholder.html', {'not': notifications})

    return redirect('/login/')


def contact_page(request):
    notifications = template_refresh_notifications(request)
    return render(request, 'ContactPage.html', {'not': notifications})


def lecturers_page(request):
    notfications = template_refresh_notifications(request)
    lecturers = models.Lecturer.objects.all()
    if len(lecturers) != 0:
        return render(request, 'LecturersPage.html', {'not': notfications, 'lec': lecturers})
    return redirect('/')


def courses_page(request):
    notfications = template_refresh_notifications(request)
    lecturer = models.Lecture.objects.all()
    lecturer_course = []

    if len(lecturer) != 0:
        for i in lecturer:
            if i.is_course:
                lecturer_course.append(i)

        if len(lecturer_course) != 0:
            return render(request, 'CoursesPage.html', {'not': notfications, 'lec': lecturer_course})

    return redirect('/')


def lectures_page(request):
    notfications = template_refresh_notifications(request)
    lecturer = models.Lecture.objects.all()
    lecturer_course = []

    if len(lecturer) != 0:
        for i in lecturer:
            if not i.is_course:
                lecturer_course.append(i)

        if len(lecturer_course) != 0:
            return render(request, 'LecturesPage.html', {'not': notfications, 'lec': lecturer_course})

    return redirect('/')


def lecturer_page(request, id):
    notifications = template_refresh_notifications(request)

    if models.Lecturer.objects.filter(id=id).exists():
        lecturer = models.Lecturer.objects.get(id=id)
        return render(request, 'LecturerPage.html', {
            'not': notifications,
            'lec': lecturer,
            'image': f'Media/{lecturer.picture.name}'
        })

    return redirect('/')


def faq_page(request):
    notifications = template_refresh_notifications(request)
    return render(request, 'FaqPage.html', {'not': notifications})


def view_payment_confirmation(request, cpf):
    if request.user.is_authenticated and request.user.is_staff:
        if models.UserPersonalData.objects.filter(cpf=cpf).exists():
            personal_data = models.UserPersonalData.objects.get(cpf=cpf)
            if hasattr(personal_data, 'sub_confirmation'):
                pc = personal_data.sub_confirmation
                image = pc.payment_confirmation
                return render(request, 'PaymentConfirmationPage.html', {'image': 'Media/'+image.name})

            return HttpResponse('Não foi encontrado um comprovante para a pessoa informada')

        return HttpResponse(f'Não foi encontrada a pessoa informada {models.UserPersonalData.objects.filter(cpf=cpf).exists()}')

    return redirect('/')


def payment_confirmation_page(request):
    if request.user.is_staff:
        form = forms.SubscriptionConfirmationForm()
        all_payment_confirmations = models.SubscriptionPaymentConfirmation.objects.all()
        payment_confirmations = []

        for i in all_payment_confirmations:
            if not hasattr(i, 'subscription'):  # Garante que só apareça os que ainda não tem inscrição confirmada
                payment_confirmations.append(i)

        if request.POST:
            form = forms.SubscriptionConfirmationForm(data=request.POST)

            if form.is_valid():
                cpf = form.cleaned_data.get('cpf')
                sub_type = form.cleaned_data.get('subscription_type')

                if models.UserPersonalData.objects.filter(cpf=cpf).exists():
                    user_cpf = models.UserPersonalData.objects.get(cpf=cpf)
                    if models.SubscriptionPaymentConfirmation.objects.filter(user_cpf=user_cpf).exists():
                        payment_confirmation_from_db = models.SubscriptionPaymentConfirmation.objects.get(
                            user_cpf=user_cpf)

                        subscripton = models.Subscription(
                            user_cpf=user_cpf,
                            type=sub_type,
                            payment_confirmation=payment_confirmation_from_db,
                            date_of_verification=datetime.date.today(),
                        )

                        subscripton.save()
                        return redirect('/payment-confirmation-panel/')

                    else:
                        messages.error(request, 'CPF não possui arquivo de confirmação')
                else:
                    messages.error(request, 'CPF digitado inexistente na DB')

        return render(request, 'SubscriptionConfirmationPage.html', {'form': form, 'pc': payment_confirmations})

    return redirect('/')


def reset_password_send_code(request):
    if not request.user.is_authenticated:
        form = forms.ResetPasswordSendCodeForm()

        if request.POST:
            form = forms.ResetPasswordSendCodeForm(data=request.POST)

            if form.is_valid():
                email = form.cleaned_data.get('email')

                if models.SemacUser.object.filter(email=email).exists():
                    user = models.SemacUser.object.get(email=email)

                    if not hasattr(user, 'password_code'):
                        code = generate_validation_code()
                        semac_password_code = models.SemacUserPasswordCode(
                            code=code,
                            user_email=user,
                        )
                        semac_password_code.save()

                        write_to_smtp_password_queue(user.email, code)

                    return redirect('/reset-password-with-code/')

                messages.error(request, 'Email informado não possui conta cadastrada!')

            return render(request, 'ResetPasswordSendCodePage.html', {'form': form})

        return render(request, 'ResetPasswordSendCodePage.html', {'form': form})

    return redirect('/')


def reset_password_with_code(request):
    if not request.user.is_authenticated:
        form = forms.ResetPasswordWithCodeForm()

        if request.POST:
            form = forms.ResetPasswordWithCodeForm(data=request.POST)

            try:
                if form.is_valid():
                    email = form.cleaned_data.get('email')
                    code = form.cleaned_data.get('code')
                    password = form.clean_and_verify_password()

                    if models.SemacUser.object.filter(email=email).exists():
                        user = models.SemacUser.object.get(email=email)

                        if hasattr(user, 'password_code'):
                            user_code = user.password_code

                            if user_code.code == code:
                                user.set_password(password)
                                user.save()
                                user_code.delete()
                                return redirect('/login/')

                            messages.error(request, 'Código informado não é o mesmo enviado no seu e-mail')

                        else:
                            redirect('/reset-password/')

                    else:
                        messages.error(request, 'Email informado não possui conta cadastrada')

            except PasswordNotEqualException:
                messages.error(request, 'Senhas digitadas não são iguais')

            except SmallPasswordException:
                messages.error(request, 'A senha informada precisa de pelo menos 8 caracteres')

        return render(request, 'ResetPasswordWithCodePage.html', {'form': form})

    return redirect('/')


def tournament_page(request):
    notifications = template_refresh_notifications(request)
    return render(request, 'TournamentPage.html', {'not': notifications})
