from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout

from . import forms, models

def DEBUG_render_test(request):
    if request.POST:
        form = forms.SemacUserLoginForm(data=request.POST)
        if form.is_valid():
            answer = request.POST
            login(request, form.get_user())
            #form.save()
            return render(request, 'TestingForms.html', {'form': form, 'answer': answer})
    answer = ['nada']
    form = forms.PersonalDataForm()
    return render(request, 'TestingForms.html', {'form': form, 'answer': answer})


def DEBUG_testing_mesures(request):
    if request.user.is_authenticated:
        return render(request, 'TestingThreads.html', {'nome': request.user.email})
    return render(request, 'TestingThreads.html', {'nome': 'a'})

