from django.shortcuts import render
from django.http import HttpResponse


def DEBUG_render_test(request):
    return HttpResponse('<h1>Hello World!<\h1>')

