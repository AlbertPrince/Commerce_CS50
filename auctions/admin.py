from django.contrib import admin

from .models import *

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "message", "author", "listing"]

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)
admin.site.register(Bid)
