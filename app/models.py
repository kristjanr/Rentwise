from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djplaces.fields import LocationField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook_id = models.TextField(max_length=500)
    picture_url = models.TextField(max_length=500)
    place = models.CharField(max_length=250, null=True)
    location = LocationField(base_field='place', null=True)

    @property
    def facebook_url(self):
        return 'https://www.facebook.com/%s/' % self.facebook_id

    def __str__(self):
        return self.user.__str__() + ' ' + self.facebook_url


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


positive_decimal = MinValueValidator(Decimal('0.01'))
min_1 = MinValueValidator(1)
max_500 = MaxValueValidator(500)


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )

    renters = models.ManyToManyField(User, related_name='items')

    categories = models.ManyToManyField(Category, related_name='items')

    name = models.CharField(max_length=100, validators=[MinLengthValidator(5)])

    description = models.CharField(max_length=5000, validators=[MinLengthValidator(20)])

    price_per_day = models.DecimalField(verbose_name='price £/day', max_digits=4, decimal_places=2,
                                        validators=[positive_decimal])

    minimum_rental_period = models.IntegerField(verbose_name='min. days',
                                                validators=[min_1, max_500])

    estimated_value = models.DecimalField(verbose_name='value £', max_digits=8, decimal_places=2,
                                          validators=[positive_decimal])

    place = models.CharField(max_length=250)

    location = LocationField(base_field='place')

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True, verbose_name='Added on')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/item/%i/" % self.id


class Image(models.Model):
    item = models.ForeignKey('item', on_delete=models.CASCADE, )
    url = models.URLField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.url
