from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AddItemTest(TestCase):
    fixtures = ['categories', 'auth', 'profile']

    def test_require_login(self):
        response = self.client.get(reverse('add_item'), follow=True)
        self.assertEqual(response.redirect_chain[0], (reverse('login') + '?next=' + reverse('add_item'), 302))

    def test_add_item_get(self):
        self.client.force_login(User.objects.get(id=1))

        response = self.client.get(reverse('add_item'))

        self.assertContains(response, '')
        self.assertTemplateUsed(response, 'app/add_item.html')
