from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from archive.forms import ImageCollectionForm, ImageForm
from archive.models import Image
from helpers.decorators import admin_required
from helpers.model import is_owner
from home.models import Collection


def archive_collection(request):
    archive_collection_objs = Collection.objects.filter(
        collection_type='image'
    ).order_by('-updated_at')
    context = {
        'title': 'Acervo',
        'db_regs': archive_collection_objs,
        'search_url': '',
    }
    return render(request, 'archive/pages/archive.html', context)


@login_required
@admin_required
def create_archive_collection(request):
    form = ImageCollectionForm(request.POST or None, request.FILES or None)
    image_form = ImageForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Criar coleção de imagens',
        'form': form,
        'image_form': image_form,
    }
    if request.POST:
        images = request.FILES.getlist('images')
        if form.is_valid():
            if not images:
                messages.error(request, 'Nenhum arquivo foi selecionado.')
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
                messages.success(request, 'Coleção de imagens criada com sucesso.')
                return redirect(reverse('archive:archive'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'archive/pages/create-archive.html', context)


def view_archive_collection(request, slug):
    archive_collection_obj = get_object_or_404(Collection, slug=slug)
    context = {
        'title': archive_collection_obj.title,
        'archive_collection': archive_collection_obj,
        'is_owner': is_owner(request.user, archive_collection_obj),
    }
    return render(request, 'archive/pages/view-archive.html', context)


@login_required
@admin_required
def delete_archive_collection(request, slug):
    archive_collection_obj = get_object_or_404(Collection, slug=slug)
    if not is_owner(request.user, archive_collection_obj):
        raise PermissionDenied()
    archive_collection_obj.delete()
    messages.success(request, 'Coleção de imagens apagada com sucesso.')
    return redirect(reverse('archive:archive'))


@login_required
@admin_required
def delete_image(request, pk):
    image_obj = get_object_or_404(Image, pk=pk)
    if not is_owner(request.user, image_obj.collection):
        raise PermissionDenied()
    image_obj.delete()
    if image_obj.collection.get_images.exists():
        messages.success(request, 'Imagem apagada com sucesso.')
        return redirect(
            reverse('archive:view_archive', kwargs={'slug': image_obj.collection.slug})
        )
    image_obj.collection.delete()
    messages.success(request, 'Coleção de imagens apagada com sucesso.')
    return redirect(reverse('archive:archive'))


@login_required
@admin_required
def edit_archive_collection(request, slug):
    archive_collection_obj = get_object_or_404(Collection, slug=slug)
    form = ImageCollectionForm(
        request.POST or None, request.FILES or None, instance=archive_collection_obj
    )
    image_form = ImageForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Editar coleção de imagens',
        'form': form,
        'image_form': image_form,
        'is_editing': True,
    }
    if request.POST:
        if form.is_valid():
            images_to_remove_ids = [
                k.split('-')[-1]
                for k, v in request.POST.items()
                if k.startswith('image-') and v == 'yes'
            ]
            images = request.FILES.getlist('images')
            archive_collection = form.save()
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
            return redirect(reverse('archive:archive'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'archive/pages/edit-archive.html', context)
