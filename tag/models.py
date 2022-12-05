import string
from random import SystemRandom

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    nome = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Here start the fields to generic relation

    # It is model representation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # It is id representation the model above
    object_id = models.CharField()

    # It is a field representation that know above fields
    # (content_type, object_id)
    content_object = GenericForeignKey('content_type', 'object_id')

    # It is a method to make a unique slug to our model
    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choice(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    # It is only to we get a string
    def __str__(self):
        return self.name
