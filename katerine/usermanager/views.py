from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from . import forms, models


def homepage(request):
    return render(request, 'Homepage.html', {})


def loginpage(request):

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


def logoutpage(request):
    logout(request)
    return redirect('/')


def profilepage(request):
    if request.user.is_authenticated:
        try:
            personal_data = models.UserPersonalData.objects.get(user_email=request.user)
            lectures = models.PersonOnLecture.objects.filter(user_cpf=personal_data).all()
            return render(request, 'Profile.html', {'pd': personal_data, 'lc': lectures})
        except ObjectDoesNotExist:
            return redirect('/debug/')
    return redirect('/login/')


def registerpage(request):
    if request.POST:
        form = forms.SemacUserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/debug/')
        return render(request, 'Register.html', {'form': form})
    form = forms.SemacUserRegisterForm()
    return render(request, 'Register.html', {'form': form})


def personaldatapage(request):
    pass


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

