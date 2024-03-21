from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('competicoes/', include('competitions.urls')),
    path('noticias/', include('news.urls')),
    path('edicoes/', include('editions.urls')),
    path('acervo/', include('archive.urls')),
    path('documentos/', include('documents.urls')),
    path('', include('users.urls')),
    path('', include('social_django.urls'), name='social'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))

handler404 = 'handlers.views.page_not_found_404'
handler500 = 'handlers.views.server_error_500'
handler403 = 'handlers.views.permission_denied_403'
handler400 = 'handlers.views.bad_request_400'
