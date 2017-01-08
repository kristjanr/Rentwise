from django.conf.urls import url

from app.views import signed_up_users, add_item, home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^signed-up-users', signed_up_users, name='signed-up-users'),
    url(r'^item/add$', add_item, name='add_item'),
]
