from django.contrib.auth.models import User
from django.test import TestCase
from django.test import tag
from django.urls import reverse

from app.models import Item, Profile


@tag('separate')
class ViewItemTest(TestCase):
    fixtures = ['categories', 'auth', 'items']

    def test_view_item_requires_login(self):
        view_first_item_url = reverse('view_item', kwargs=dict(pk=1))
        response = self.client.get(view_first_item_url, follow=True)
        self.assertEqual(response.redirect_chain[0], (reverse('login') + '?next=' + view_first_item_url, 302))

    def test_view_item_ok(self):
        self.client.force_login(User.objects.get(id=1))

        response = self.client.get(reverse('view_item', kwargs=dict(pk=1)))

        self.assertContains(response, 'First Item Name is Here, yes!', status_code=200)

    def test_view_item_not_exists(self):
        self.client.force_login(User.objects.get(id=1))

        response = self.client.get(reverse('view_item', kwargs=dict(pk=3)))

        self.assertContains(response, 'Page not found', status_code=404)

    def test_publish_item(self):
        self.client.force_login(User.objects.get(id=1))
        item = Item.objects.get(id=1)
        item.is_published = False
        item.save()
        self.assertFalse(Item.objects.get(id=1).is_published)

        response = self.client.post(reverse('publish_item', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(response.redirect_chain[0], (reverse('view_item', kwargs=dict(pk=1)), 302))
        self.assertTrue(Item.objects.get(id=1).is_published)

    def test_unpublish_item(self):
        self.client.force_login(User.objects.get(id=1))
        self.assertTrue(Item.objects.get(id=1).is_published)

        response = self.client.post(reverse('unpublish_item', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(response.redirect_chain[0], (reverse('view_item', kwargs=dict(pk=1)), 302))
        self.assertFalse(Item.objects.get(id=1).is_published)

    def test_delete_item(self):
        self.client.force_login(User.objects.get(id=1))

        response = self.client.post(reverse('delete_item', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(response.redirect_chain[0], (reverse('home'), 302))
        self.assertEqual(len(Item.objects.filter(id=1)), 0)

    def test_contact_owner(self):
        user = User.objects.get(id=1)
        # This if/else is here because of what seems to be a quirk by Django:
        # Profile exists, when running this TestCase class separately,
        # but Profile does not exist when running all the tests together (python manage.py test)
        if len(Profile.objects.all()) == 0:
            profile = Profile(id=1, user=user)
        else:
            profile = Profile.objects.get(user=user)
        profile.facebook_id = '1595851600430548'
        profile.save()
        self.client.force_login(user)

        response = self.client.post(reverse('contact_owner', kwargs=dict(pk=1)), follow=True)

        self.assertEqual(response.redirect_chain[0], ('https://www.facebook.com/1595851600430548/', 302))
