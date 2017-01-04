from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def home(request):
    return redirect('/login/facebook')


@login_required
def signed_up_users(request):
    users = User.objects.all()
    context = dict(users=users)
    return render(request, 'app/users.html', context=context)


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        if user.username == 'KristjanRoosild':
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
        profile = user.profile
        profile.facebook_id = response.get('id')
        profile.save()
