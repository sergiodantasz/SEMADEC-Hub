from django.db import models


class News(models.Model):
    administrator = models.ForeignKey(
        'users.Administrator',
        on_delete=models.SET_NULL,
        null=True,
        db_column='administrator_id',
    )
    title = models.CharField(
        max_length=200,
    )
    excerpt = models.CharField(
        max_length=200,
    )
    cover = models.ImageField(
        upload_to='',  # CHANGE IT LATER.
        default='/base/static/global/img/news_cover_placeholder.jpg',  # REVIEW LATER
    )
    content = models.TextField()  # Does it need to be tested?
    slug = models.SlugField(
        max_length=225,
        unique=True,
    )
    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
