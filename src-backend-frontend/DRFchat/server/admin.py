from django.contrib import admin
from .models import Channel, Server, Category

models = [Channel, Server, Category]
for model in models:
    admin.site.register(model)