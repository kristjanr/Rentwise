from django.conf.urls import url

from app.views import signed_up_users, home

urlpatterns = [
    url(r'^$', home, name='index'),
    url(r'^signed-up-users', signed_up_users, name='signed-up-users'),
]
