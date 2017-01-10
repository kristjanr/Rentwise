from django.conf.urls import url
from django.views.generic import TemplateView

from app.views import ImageUploadView, ItemAddView, ItemDetailView, ItemDeleteView, publish_item, \
    unpublish_item, logout_view, home, contact_owner, add_location

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^item/add$', ItemAddView.as_view(), name='add_item'),
    url(r'^item/(?P<pk>[0-9]+)/$', ItemDetailView.as_view(), name='view_item'),
    url(r'^item/(?P<pk>[0-9]+)/images$', ImageUploadView.as_view(), name='upload_images'),
    url(r'^item/(?P<pk>[0-9]+)/delete$', ItemDeleteView.as_view(), name='delete_item'),
    url(r'^item/(?P<pk>[0-9]+)/publish', publish_item, name='publish_item'),
    url(r'^item/(?P<pk>[0-9]+)/unpublish', unpublish_item, name='unpublish_item'),
    url(r'^item/(?P<pk>[0-9]+)/contact-owner', contact_owner, name='contact_owner'),
    url(r'^logout/facebook', logout_view, name='logout'),
    url(r'^login/$', TemplateView.as_view(template_name='app/log_in.html'), name='login'),
    url(r'^location/add', add_location, name='add_location'),
    url(r'^terms$', TemplateView.as_view(template_name='app/terms.html'), name='terms'),
]
