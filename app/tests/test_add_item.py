from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from app.models import Item


class AddItemTest(TestCase):
    fixtures = ['categories', 'auth', 'profile']

    def test_require_login(self):
        response = self.client.get(reverse('add_item'), follow=True)
        self.assertEqual(response.redirect_chain[0], (reverse('login') + '?next=' + reverse('add_item'), 302))

    def test_add_item_get(self):
        self.client.force_login(User.objects.get(id=1))

        response = self.client.get(reverse('add_item'))

        self.assertContains(response, '', status_code=200)
        self.assertTemplateUsed(response, 'app/add_item.html')

    def test_add_item_post_ok(self):
        self.client.force_login(User.objects.get(id=1))

        item_data = dict(
            categories=(1, 2, 3),
            name='12345',
            description='12345678901234567890',
            price_per_day=0.01,
            minimum_rental_period=1,
            estimated_value=1,
            place='5 Trafalgar Square, London WC2N 5NJ, UK',
            location=(51.508039, -0.12806899999998222),
            image01='https://ybuy.s3-eu-west-2.amazonaws.com/uploads%2Fimages%2F3eb3e174-e5fa-11e6-9116-f45c8991cf33.gif',

        )
        response = self.client.post(reverse('add_item'), item_data, follow=True)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Item Added')
        self.assertEqual(response.redirect_chain[0], (reverse('view_item', kwargs=dict(pk=1)) + '?new=true', 302))
        self.assertTemplateUsed(response, 'app/item_details.html')
        self.assertNotContains(response, 'This field is required.')
        self.assertContains(
            response,
            'Your item has been uploaded successfully! It is currently unpublished and will be reviewed within 24 hours.',
            1)
        self.assertFalse(Item.objects.get(id=1).is_published)

    def test_add_item_post_not_ok(self):
        self.client.force_login(User.objects.get(id=1))

        item_data = dict(
            categories=(1, 2, 3),
            name='1234',
            description='12345678901234567890',
            price_per_day=0.01,
            minimum_rental_period=1,
            estimated_value=1,
            place='5 Trafalgar Square, London WC2N 5NJ, UK',
            location=(51.508039, -0.12806899999998222),
            image01='https://ybuy.s3-eu-west-2.amazonaws.com/uploads%2Fimages%2F3eb3e174-e5fa-11e6-9116-f45c8991cf33.gif',

        )
        response = self.client.post(reverse('add_item'), item_data)

        self.assertNotContains(response, 'This field is required.')
        self.assertEqual(len(Item.objects.all()), 0)
