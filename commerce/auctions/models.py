from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Users of the application."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    """Categories a listing can belong to."""
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'


class Listing(models.Model):
    """Listings for sale or for auction."""
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    starting_bid = models.FloatField()
    current_bid = models.FloatField()
    description = models.CharField(max_length=1024)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.URLField(max_length=256, blank=True)
    watchers = models.ManyToManyField(User, on_delete=models.CASCADE, related_name='watching')

    def __str__(self):
        return f'{self.pk}: {self.title}'


class Bid(models.Model):
    """Bids for listings submitted by users."""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User {self.user} bid on listing {self.listing}'


class Comment(models.Model):
    """Comments on a listing submitted by users."""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='comments')
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment submitted by user {self.user} on listing {self.listing}'
