from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


def home(request):
    return render(request, 'app/index.html')


@login_required
def signed_up_users(request):
    users = User.objects.all()
    context = dict(users=users)
    return render(request, 'app/users.html', context=context)


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


@login_required
def add_item(request):
    return render(request, 'app/add_item.html')
