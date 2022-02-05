import django.forms as forms
from .models import Listing, Comment


class ListingForm(forms.ModelForm):
    """Listings for sale or for auction."""

    class Meta:
        model = Listing
        fields = ["title", "starting_bid", "description", "category", "image"]


class CommentForm(forms.ModelForm):
    """Comment on a listing as a user."""

    class Meta:
        model = Comment
        fields = ["comment"]
