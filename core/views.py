from django.shortcuts import redirect, render


def index_view(request):
    if request.user.is_authenticated:
        return redirect('contas:perfil')

    return render(request, 'core/index.html')