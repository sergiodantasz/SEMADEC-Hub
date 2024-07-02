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
        context = {
            'title': 'Criar coleção de imagens',
            'image_form': self.get_image_form(),
        }
        return super().get_context_data(**context)

    def form_valid(self, form):
        image_form = self.get_image_form()
        if image_form.is_valid():
            images = self.request.FILES.getlist('images')
            if not images:
                messages.error(self.request, self.msg['error']['image'])
                # Raise exception
                # Idea: create a method that first check if other form has error and
                # then run form_valid()
            archive_collection = form.save(commit=False)  # type: ignore
            archive_collection.administrator = self.request.user
            archive_collection.save()
            form.save_m2m()  # type: ignore
            for image in images:
                Image.objects.create(
                    collection=archive_collection,
                    content=image,
                )
        return super().form_valid(form)


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
        context = {
            'title': 'Editar coleção de imagens',
            'image_form': self.get_image_form(),
            'is_editing': True,
        }
        return super().get_context_data(**context)

    def form_valid(self, form):
        image_form = self.get_image_form()
        if image_form.is_valid():
            images = self.request.FILES.getlist('images')
            images_to_remove_ids = [
                k.split('-')[-1]
                for k, v in self.request.POST.items()
                if k.startswith('image-') and v == 'yes'
            ]
            images = self.request.FILES.getlist('images')
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
                archive_collection.delete()  # Not working
                messages.success(
                    self.request, 'Coleção de imagens apagada com sucesso.'
                )
        return super().form_valid(form)
