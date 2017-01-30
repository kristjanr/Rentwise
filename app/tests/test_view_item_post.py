from django.contrib.auth.models import User
from django.test import TestCase
from django.test import tag
from django.urls import reverse

from app.models import Item, Profile


def get_user_and_add_facebook_id():
    owner = User.objects.get(id=1)
    # This if/else is here because of what seems to be a quirk by Django:
    # Profile exists, when running this TestCase class separately,
    # but Profile does not exist when running all the tests together (python manage.py test)
    if len(Profile.objects.all()) == 0:
        owner_profile = Profile(id=1, user=owner)
    else:
        owner_profile = Profile.objects.get(user=owner)
    owner_profile.facebook_id = 'foo'
    owner_profile.save()
    return owner


@tag('separate')
class ViewItemPostTest(TestCase):
    fixtures = ['categories', 'users', 'items']

    def test_staff_publishes_item(self):
        self.client.force_login(User.objects.get(id=3))
        item = Item.objects.get(id=1)
        item.is_published = False
        item.save()
        self.assertFalse(Item.objects.get(id=1).is_published)

        response = self.client.post(reverse('publish_item', kwargs=dict(pk=1)), follow=True)

        self.assertTrue(Item.objects.get(id=1).is_published)
        self.assertEqual(response.redirect_chain[0], (reverse('view_item', kwargs=dict(pk=1)), 302))

    def test_non_staff_tries_publish_item(self):
        self.client.force_login(User.objects.get(id=1))
        item = Item.objects.get(id=1)
        item.is_published = False
        item.save()
        self.assertFalse(Item.objects.get(id=1).is_published)

        self.client.post(reverse('publish_item', kwargs=dict(pk=1)), follow=True)

        self.assertFalse(Item.objects.get(id=1).is_published)

    def test_staff_unpublishes_item(self):
        self.client.force_login(User.objects.get(id=3))
        self.assertTrue(Item.objects.get(id=1).is_published)

        response = self.client.post(reverse('unpublish_item', kwargs=dict(pk=1)), follow=True)

        self.assertFalse(Item.objects.get(id=1).is_published)
        self.assertEqual(response.redirect_chain[0], (reverse('view_item', kwargs=dict(pk=1)), 302))

    def test_non_staff_tries_unpublish_item(self):
        self.client.force_login(User.objects.get(id=1))
        self.assertTrue(Item.objects.get(id=1).is_published)

        self.client.post(reverse('unpublish_item', kwargs=dict(pk=1)), follow=True)

        self.assertTrue(Item.objects.get(id=1).is_published)

    def test_owner_deletes_item(self):
        self.client.force_login(User.objects.get(id=1))

        response = self.client.post(reverse('delete_item', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(len(Item.objects.filter(id=1)), 0)
        self.assertEqual(response.redirect_chain[0], (reverse('home'), 302))

    def test_staff_deletes_item(self):
        self.client.force_login(User.objects.get(id=3))

        response = self.client.post(reverse('delete_item', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(len(Item.objects.filter(id=1)), 0)
        self.assertEqual(response.redirect_chain[0], (reverse('home'), 302))

    def test_another_user_tries_delete_item(self):
        self.client.force_login(User.objects.get(id=2))

        response = self.client.post(reverse('delete_item', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(len(Item.objects.filter(id=1)), 1)
        self.assertEqual(response.redirect_chain[0], (reverse('view_item', kwargs=dict(pk=1)), 302))

    def test_another_renter_contacts_owner(self):
        get_user_and_add_facebook_id()
        renter = User.objects.get(id=2)
        self.client.force_login(renter)

        response = self.client.post(reverse('contact_owner', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(response.redirect_chain[0], ('https://www.facebook.com/foo/', 302))
        self.assertEqual(len(Item.objects.get(id=1).renters.all()), 1)

    def test_same_owner_contacts_owner(self):
        owner = get_user_and_add_facebook_id()
        self.client.force_login(owner)

        response = self.client.post(reverse('contact_owner', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(response.redirect_chain[0], ('https://www.facebook.com/foo/', 302))
        self.assertEqual(len(Item.objects.get(id=1).renters.all()), 0)

    def test_staff_contacts_owner(self):
        get_user_and_add_facebook_id()
        staff = User.objects.get(id=3)
        self.client.force_login(staff)

        response = self.client.post(reverse('contact_owner', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(response.redirect_chain[0], ('https://www.facebook.com/foo/', 302))
        self.assertEqual(len(Item.objects.get(id=1).renters.all()), 0)
