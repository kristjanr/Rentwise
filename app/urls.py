from django.conf.urls import url

from app.views import ImageUploadView, ItemView, ItemDetailView, ItemDeleteView, publish_item, \
    unpublish_item, logout_view, home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^item/add$', ItemView.as_view(), name='add_item'),
    url(r'^item/(?P<pk>[0-9]+)/$', ItemDetailView.as_view(), name='view_item'),
    url(r'^item/(?P<pk>[0-9]+)/images$', ImageUploadView.as_view(), name='upload_images'),
    url(r'^item/(?P<pk>[0-9]+)/delete$', ItemDeleteView.as_view(), name='delete_item'),
    url(r'^item/(?P<pk>[0-9]+)/publish', publish_item, name='publish_item'),
    url(r'^item/(?P<pk>[0-9]+)/unpublish', unpublish_item, name='unpublish_item'),
    url(r'^logout/facebook', logout_view, name='logout'),
]
