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
    form = forms.SemacUserLoginForm()
    return render(request, 'TestingForms.html', {'form': form, 'answer': answer})

