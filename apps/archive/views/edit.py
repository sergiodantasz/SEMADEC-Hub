from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from apps.archive.forms import ImageCollectionForm, ImageForm
from apps.archive.models import Image
from apps.home.models import Collection
from base.views import BaseCreateView, BaseDeleteView, BaseEditView
from helpers.decorators import admin_required
from helpers.model import is_owner


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ArchiveImageDeleteView(BaseDeleteView):
    model = Image
    msg = {
        'success': {'form': 'Imagem removida com sucesso.'},
        'error': {'form': 'Não foi possível remover esta imagem.'},
    }

    def get(self, request, *args, **kwargs):
        image_obj: Image = self.get_object()  # type: ignore
        if not is_owner(request.user, image_obj.collection):
            raise PermissionDenied()
        image_obj.delete()
        if image_obj.collection.get_images.exists():
            messages.success(request, 'Imagem apagada com sucesso.')
            return redirect(
                reverse('archive:detail', kwargs={'slug': image_obj.collection.slug})
            )
        image_obj.collection.delete()
        messages.success(request, 'Coleção de imagens apagada com sucesso.')
        return redirect(reverse('archive:home'))


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ArchiveDeleteView(BaseDeleteView):
    model = Collection
    msg = {
        'success': {'form': 'Coleção de imagens removida com sucesso.'},
        'error': {'form': 'Não foi possível remover esta coleção de imagens.'},
    }


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
        image_form = self.image_form(
            self.request.POST or None, self.request.FILES or None
        )
        return image_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context |= {
            'title': 'Criar coleção de imagens',
            'image_form': self.get_image_form(),
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        image_form = self.get_image_form()
        images = request.FILES.getlist('images')
        if form.is_valid() and image_form.is_valid():
            if not images:
                messages.error(request, self.msg['error']['image'])
                return super().get(self.request, *args, **kwargs)
            else:
                archive_collection = form.save(commit=False)  # type: ignore
                archive_collection.administrator = request.user
                archive_collection.save()
                form.save_m2m()  # type: ignore
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


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ArchiveEditView(BaseEditView):
    form_class = ImageCollectionForm
    image_form = ImageForm
    template_name = 'archive/pages/edit-archive.html'
    msg = {
        'success': {'form': 'Coleção de imagens editada com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'image': 'Nenhum arquivo foi selecionado.',
        },
    }

    def get_image_form(self, form_class=None):
        image_form = self.image_form(
            self.request.POST or None, self.request.FILES or None
        )
        return image_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context |= {
            'title': 'Editar coleção de imagens',
            'image_form': self.get_image_form(),
            'is_editing': True,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        image_form = self.get_image_form()
        ...
        images = request.FILES.getlist('images')
        if form.is_valid() and image_form.is_valid():
            images_to_remove_ids = [
                k.split('-')[-1]
                for k, v in request.POST.items()
                if k.startswith('image-') and v == 'yes'
            ]
            images = request.FILES.getlist('images')
            archive_collection = form.save()  # type: ignore
            for image in images:
                Image.objects.create(
                    collection=archive_collection,
                    content=image,
                )
            for image_id in images_to_remove_ids:
                image = Image.objects.get(id=image_id)
                image.delete()
            if not archive_collection.get_images.exists():
                archive_collection.delete()
                messages.success(request, 'Coleção de imagens apagada com sucesso.')
            else:
                messages.success(request, 'Coleção de imagens editada com sucesso.')
            return redirect(self.get_success_url())
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
            return super().get(self.request, *args, **kwargs)
