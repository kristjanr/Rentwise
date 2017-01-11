from django.contrib import admin

from app.models import Item, Profile, Category, Image

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Image)
