from django.conf.urls import url

from app.views import logged_in, home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^logged-in', logged_in, name='logged-in'),
]
