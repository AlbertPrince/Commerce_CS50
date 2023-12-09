from django import forms
from django.forms import ModelForm
from .models import AuctionListing, Comment, Bid

class AuctionForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = '__all__'
        exclude = ["seller", "is_active", "current_bid", "creator"]
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_price"]