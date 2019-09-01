from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, SmartResize
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
import os
from utils.utils import has_changed


class Categoria(models.Model):
    descricao = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.descricao


class Todo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.titulo


# @receiver(pre_save, sender=Todo)
# def handler_pre_save_todo(sender, instance, update_fields, **kwargs):
#     instance.user = User


class Imagem(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    imagem = ProcessedImageField(
        upload_to='todo/%Y-%m',
        processors=[SmartResize(width=1920, height=1080, upscale=False)],
        format='JPEG',
        options={'quality': 70},
    )
    thumbnail = ImageSpecField(
        source='imagem',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 60}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, **kwargs):
        # orig = None if self.pk is None else Imagem.objects.get(pk=self.pk)
        # if orig and orig.imagem != self.imagem:
        #     kwargs['update_fields'] = ['imagem']

        if self.pk and has_changed(self, 'imagem'):
            kwargs['update_fields'] = ['imagem']
        super().save(**kwargs)


@receiver(pre_delete, sender=Imagem)
def handler_pre_delete_image(instance, **kwargs):
    os.path.exists(instance.imagem.path) and os.remove(instance.imagem.path)


@receiver(pre_save, sender=Imagem)
def handler_pre_save_image(sender, instance, update_fields, **kwargs):
    if update_fields and 'imagem' in update_fields:
        orig = sender.objects.get(pk=instance.pk)
        os.path.exists(orig.imagem.path) and os.remove(orig.imagem.path)
