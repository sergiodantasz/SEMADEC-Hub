from django.db import models


class Collection(models.Model):
    COLLECTION_TYPE_CHOICES = {
        'document': 'Documento',
        'image': 'Imagem',
    }

    administrator = models.ForeignKey(
        'users.Administrator',
        on_delete=models.SET_NULL,
        null=True,
        db_column='administrator_id',
    )
    files = models.ManyToManyField(
        to='archive.File',
    )
    title = models.CharField(
        unique=True,
        max_length=200,
    )
    type = models.CharField(
        max_length=10,
        choices=COLLECTION_TYPE_CHOICES,
    )
    cover = models.ImageField(
        upload_to='',  # CHANGE IT LATER.
        # default='/base/static/global/img/collection_cover_placeholder.jpg',
        # REVIEW LATER
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        max_length=225,
    )
    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def get_files(self):
        return self.files.all()

    def __str__(self):
        return str(self.title)


class File(models.Model):
    display_name = models.CharField(
        max_length=225,
        null=True,
        blank=True,
    )
    content = models.FileField(
        unique=True,
        db_column='path',
    )

    def __str__(self):
        return str(self.content.name)
