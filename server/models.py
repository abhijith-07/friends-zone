from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .validators import validate_icon_image_size, validate_image_file_extension


def category_icon_path(instance, filename):
    return f"category/{instance.id}/icon/{filename}"


def server_icon_path(instance, filename):
    return f"server/{instance.id}/icon/{filename}"


def server_banner_path(instance, filename):
    return f"server/{instance.id}/banner/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_icon_path,
        blank=True,
        null=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    def save(self, *args, **kwargs):
        if self.id:
            this = get_object_or_404(Category, id=self.id)
            if this.icon != self.icon:
                this.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(models.signals.pre_delete, sender="server.Category")
def category_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "icon":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    description = models.TextField(null=True, blank=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)
    icon = models.ImageField(
        upload_to=server_icon_path,
        blank=True,
        null=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )
    banner = models.ImageField(upload_to=server_banner_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id:
            this = get_object_or_404(Server, id=self.id)
            if this.icon != self.icon:
                this.icon.delete(save=False)
            if this.banner != self.banner:
                this.banner.delete(save=False)
        super(Server, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}-{self.id}"


@receiver(models.signals.pre_delete, sender="server.Server")
def server_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "icon" or field.name == "banner":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
