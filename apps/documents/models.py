from django.db import models


class Document(models.Model):
    collection = models.ForeignKey(
        'home.Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        related_name='documents',
    )
    name = models.CharField(
        max_length=100,
    )
    content = models.FileField(
        upload_to='collections/document/files',
        unique=True,
        db_column='path',
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.content.name
        return super().save(*args, **kwargs)
