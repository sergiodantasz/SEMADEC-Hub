from django.shortcuts import render


def page_not_found_404(request, exception):
    context = {
        'title': '404 - Página não encontrada',
        'error_code': '404',
        'error_description': 'Ops! Parece que esta página não foi encontrada...',
    }
    return render(request, 'handlers/pages/handler.html', context, status=404)


def server_error_500(request):
    context = {
        'title': '500 - Erro de servidor',
        'error_code': '500',
        'error_description': 'Ops! Parece que ocorreu um erro de servidor...',
    }
    return render(request, 'handlers/pages/handler.html', context, status=500)


def permission_denied_403(request, exception):
    context = {
        'title': '403 - Erro de permissão',
        'error_code': '403',
        'error_description': 'Ops! Parece que você não tem permissão para acessar esta página...',
    }
    return render(request, 'handlers/pages/handler.html', context, status=403)


def bad_request_400(request, exception):
    context = {
        'title': '400 - Erro de requisição',
        'error_code': '400',
        'error_description': 'Ops! Parece que esta requisição é inválida...',
    }
    return render(request, 'handlers/pages/handler.html', context, status=400)
