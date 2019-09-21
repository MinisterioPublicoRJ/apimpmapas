from django.db import models


class Icone(models.Model):
    # DATABASE FIELDS
    name = models.CharField(
        verbose_name='título do ícone',
        max_length=20
    )

    file_path = models.FileField(
        verbose_name='arquivo do ícone',
        upload_to='icones'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # META CLASS
    class Meta:
        verbose_name = 'ícone'

    # TO STRING METHOD
    def __str__(self):
        if self:
            return self.name
