"""
This module defines the data models for a Django application that represents a 
simple server and channel system.

The data models defined in this module are as follows:
- `Category`: Represents a category for servers.
- `Server`: Represents a server with its owner, category, description, and members.
- `Channel`: Represents a channel within a server with its owner, topic, and server association.

These models are used to build a basic server and channel system within a Django application.

Please note that the `Server` and `Channel` models have custom methods:
- `Server` has a custom string representation using the `__str__` method.
- `Channel` has a custom `save` method that converts the channel name to lowercase 
and a custom string representation using the `__str__` method.

This code relies on the Django web framework and its database models to define the 
structure of the database tables.
"""

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import (
    validate_icon_image_size, 
    validate_image_file_extension
)

def server_icon_upload_path(instance, filemene):
    return f"server/{instance.id}/server_icons/{filemene}"

def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"

def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"

# category table
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True, null = True)
    icon = models.FileField(
        null = True, 
        blank = True, 
        upload_to = category_icon_upload_path,
    )

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id = self.id)
            if existing.icon != self.icon:
                existing.delete(save = False)
            if existing.banner != self.banner:
                existing.banner.delete(save = False)
        super(Category, self).save(*args, **kwargs)
    
    @receiver(models.signals.pre_delete, sender = "server.Server")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save = False)
    
    def __str__(self):
        return self.name

# server table
class Server(models.Model):
    name = models.CharField(max_length = 100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "server_owner"
    )
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name = "server_owner"
    )
    description = models.CharField(max_length = 250, null = True, blank = True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

# channel table
class Channel(models.Model):
    name = models.CharField(max_length = 100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "channel_owner"
    )
    topic = models.CharField(max_length = 100)
    server = models.ForeignKey(
        Server,
        on_delete = models.CASCADE,
        related_name = "channel_server"
    )
    banner = models.ImageField(
        upload_to = server_banner_upload_path, 
        null = True, 
        blank = True,
        validators = [validate_image_file_extension]
    )
    icon = models.ImageField(
        upload_to = server_icon_upload_path, 
        null = True, 
        blank = True,
        validators = [validate_icon_image_size, validate_image_file_extension]
    )

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
