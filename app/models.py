from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djplaces.fields import LocationField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook_id = models.TextField(max_length=500)
    picture_url = models.TextField(max_length=500)

    @property
    def facebook_url(self):
        return 'https://www.facebook.com/%s/' % self.facebook_id


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    profile = models.ForeignKey('profile', on_delete=models.CASCADE, )
    renters = models.ManyToManyField(Profile, related_name='items')
    categories = models.ManyToManyField(Category, related_name='items')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price_per_day = models.DecimalField(verbose_name='price per day (£)', max_digits=6, decimal_places=2)
    minimum_rental_period = models.IntegerField(verbose_name='minimum rental period (days)')
    estimated_value = models.DecimalField(verbose_name='estimated value (£)', max_digits=8, decimal_places=2)
    place = models.CharField(max_length=250)
    location = LocationField(base_field='place')
