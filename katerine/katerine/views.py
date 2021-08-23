from django.shortcuts import redirect


def adminCheck(request):
    if not request.user.is_staff:
        return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    return redirect('/Zlp6LJQ8D8/')
