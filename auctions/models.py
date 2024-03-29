from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    item_image = models.URLField(blank=True, null=True)
    # close_time = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def update_current_bid(self, new_bid_price):
        self.current_bid = new_bid_price
        self.save()
    
    def __str__(self) -> str:
        return self.title

class Bid(models.Model):
    bid_price = models.FloatField(default=0.0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    bid_time = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.listing} {self.bid_price}"
    
    

class Comment(models.Model):
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
    
    
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist')
    listings = models.ManyToManyField('AuctionListing')
    
    def __str__(self) -> str:
        return f"{self.user.username}'s Watchlist"

    