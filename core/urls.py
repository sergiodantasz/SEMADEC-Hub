from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('competicoes/', include('apps.competitions.urls')),
    path('noticias/', include('apps.news.urls')),
    path('edicoes/', include('apps.editions.urls')),
    path('acervo/', include('apps.archive.urls')),
    path('documentos/', include('apps.documents.urls')),
    path('times/', include('apps.teams.urls')),
    path('', include('apps.users.urls')),
    path('', include('social_django.urls'), name='social'),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))

if settings.BROWSER_RELOAD:
    urlpatterns.append(path('__reload__/', include('django_browser_reload.urls')))

handler404 = 'apps.handlers.views.page_not_found_404'
handler500 = 'apps.handlers.views.server_error_500'
handler403 = 'apps.handlers.views.permission_denied_403'
handler400 = 'apps.handlers.views.bad_request_400'
