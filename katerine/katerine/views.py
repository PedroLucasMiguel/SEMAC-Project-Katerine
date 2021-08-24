from django.shortcuts import redirect

# Esse view é responsável por verificar se o usuário pode realmente acessar a área de admin
# Caso contrário, Rick this boy roll


def adminCheck(request):
    if not request.user.is_staff:
        return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    return redirect('/Zlp6LJQ8D8/')
