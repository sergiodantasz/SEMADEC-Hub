from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import suap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('competicoes/', include('competitions.urls')),
    path('noticias/', include('news.urls')),
    path('edicoes/', include('editions.urls')),
    path('acervo/', include('archive.urls')),
    path('documentos/', include('documents.urls')),
    path('', include('users.urls')),
    path('complete/suap/', suap, name='suap'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
