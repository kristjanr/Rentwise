from django.contrib import admin

from app.models import Item, Profile, Category, Image, Search

"""
Registering some Tables to be available in the Django admin app
"""

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Image)
admin.site.register(Search)
