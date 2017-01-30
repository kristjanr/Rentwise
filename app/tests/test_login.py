from django.test import TestCase
from django.urls import reverse

from rentwise.settings_default import LOGIN_URL_FACEBOOK


class AuthTest(TestCase):
    fixtures = ['categories', 'users']

    def test_redirect_to_login_fb(self):
        view_first_item_url = reverse('view_item', kwargs=dict(pk=1))
        response = self.client.get(view_first_item_url, follow=True)
        self.assertEqual(response.redirect_chain[0], (reverse('login') + '?next=' + view_first_item_url, 302))
        self.assertEqual(response.redirect_chain[1], (LOGIN_URL_FACEBOOK + '?next=' + view_first_item_url, 302))
        self.assertIn('https://www.facebook.com/', response.redirect_chain[2][0])
