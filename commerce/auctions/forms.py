from django.forms import ModelForm
from .models import Listing


class ListingForm(ModelForm):
    """Listings for sale or for auction."""
    class Meta:
        model = Listing
        fields = ['title', 'starting_bid', 'description', 'category', 'image']


class WatchForm(ModelForm):
    """Add or remove a listing from watchlist."""
    class Meta:
        model = Listing
        fields = ['watchers']
