from django.forms import ModelForm
from .models import AuctionListing, Comment

class AuctionForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = '__all__'
        exclude = ["seller", "current_bid"]
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]