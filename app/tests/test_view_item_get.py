from django.contrib.auth.models import User
from django.test import TestCase
from django.test import tag
from django.urls import reverse


@tag('separate')
class ViewItemGetTest(TestCase):
    fixtures = ['categories', 'users', 'items']

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
