from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from apps.archive.forms import ImageCollectionForm, ImageForm
from apps.archive.models import Image
from base.views import (
    BaseCreateView,
)
from helpers.decorators import admin_required


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ArchiveCreateView(BaseCreateView):
    form_class = ImageCollectionForm
    image_form = ImageForm
    template_name = 'archive/pages/create-archive.html'
    msg = {
        'success': {'form': 'Coleção de imagens criada com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'image': 'Nenhum arquivo foi selecionado.',
        },
    }

    def get_image_form(self, form_class=None):
        form_image = self.image_form(
            self.request.POST or None, self.request.FILES or None
        )
        return form_image

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context |= {
            'title': 'Criar coleção de imagens',
            'image_form': self.get_image_form(),
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form_image = self.get_image_form()
        images = request.FILES.getlist('images')
        if form.is_valid() and form_image.is_valid():
            if not images:
                messages.error(request, self.msg['error']['image'])
                return super().get(self.request, *args, **kwargs)
            else:
                archive_collection = form.save(commit=False)
                archive_collection.administrator = request.user
                archive_collection.save()
                form.save_m2m()
                for image in images:
                    Image.objects.create(
                        collection=archive_collection,
                        content=image,
                    )
                messages.success(request, self.msg['success']['form'])
                return redirect(self.get_success_url())
        else:
            messages.error(request, self.msg['error']['form'])
            return super().get(self.request, *args, **kwargs)
