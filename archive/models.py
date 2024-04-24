from django.db import models


class Image(models.Model):
    collection = models.ForeignKey(
        'home.Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        related_name='images',
    )
    content = models.ImageField(
        upload_to='collections/image/files',
        db_column='path',
    )

    def __str__(self) -> str:
        return self.content.name
