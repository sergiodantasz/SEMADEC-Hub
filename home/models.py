from django.db import models

from helpers.model import generate_collection_cover_path, get_object
from helpers.slug import generate_dynamic_slug


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        max_length=75,
        unique=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'name')
        tag = get_object(self.__class__, id=self.id)  # type: ignore
        if tag and self.name != tag.title:
            self.slug = generate_dynamic_slug(self, 'name')
        return super().save(*args, **kwargs)


class Collection(models.Model):
    COLLECTION_TYPE_CHOICES = (
        ('document', 'Documento'),
        ('image', 'Imagem'),
    )

    administrator = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        db_column='administrator_registration',
    )
    title = models.CharField(
        max_length=200,
    )
    collection_type = models.CharField(
        max_length=8,
        choices=COLLECTION_TYPE_CHOICES,
        db_column='type',
    )
    cover = models.ImageField(
        upload_to=generate_collection_cover_path,  # type: ignore
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        max_length=225,
    )
    tags = models.ManyToManyField(
        to='home.Tag',
        related_name='collections',
    )
    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def get_tags(self):
        return self.tags.all()

    @property
    def get_images(self):
        return self.images.all()  # type: ignore

    @property
    def get_documents(self):
        return self.documents.all()  # type: ignore

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'title')
        collection = get_object(self.__class__, id=self.id)  # type: ignore
        if collection and self.title != collection.title:
            self.slug = generate_dynamic_slug(self, 'title')
        return super().save(*args, **kwargs)
