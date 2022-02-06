import django.forms as forms
from .models import Listing, Comment, Bid


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


class BidForm(forms.ModelForm):
    """Bid on a listing as a user."""

    class Meta:
        model = Bid
        fields = ["amount"]
