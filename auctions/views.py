from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Comment, User, AuctionListing, Watchlist
from .forms import AuctionForm, CommentForm, BidForm


def index(request):
    active_listings = AuctionListing.objects.all()
    context = {'active_listings': active_listings}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            Watchlist.objects.create(user=user)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    form = AuctionForm()
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.seller = request.user
            auction_listing.save()
            return redirect('index')
    return render(request, "auctions/createListing.html", {"form": form})

@login_required
def editListing(request, id):
    # Retrieve the existing AuctionListing instance
    listing = get_object_or_404(AuctionListing, pk=id)

    # Check if the logged-in user is the seller of the listing
    if request.user != listing.seller:
        raise PermissionDenied("You don't have permission to edit this listing.")

    # Initialize the form with the instance of the listing
    form = AuctionForm(instance=listing)

    if request.method == "POST":
        form = AuctionForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))

    return render(request, "auctions/editListing.html", {"form": form, "listing": listing})


def listing(request, auction_id):
    listing = AuctionListing.objects.get(id=auction_id)
    form = BidForm()
    allComments = Comment.objects.filter(listing=listing)
    # watchlist,created = Watchlist.objects.get_or_create(user=request.user)
    # is_in_watchlist = listing in watchlist.listings.all()
    is_in_watchlist = request.user.watchlist.listings.all()
    context = {'listing': listing, "is_in_watchlist": is_in_watchlist, "form": form, "comments": allComments}
    return render(request, "auctions/listing.html", context)
 
@login_required(login_url='login')
def addToWatchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    # watchlist,created = Watchlist.objects.get_or_create(user=request.user)
    request.user.watchlist.listings.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required(login_url="login")
def deleteFromWatchlist(request, id):
    listing = AuctionListing.objects.get(id=id)
    # watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    request.user.watchlist.listings.remove(listing)
    return HttpResponseRedirect(reverse("listing", args=(id,)))       
    
@login_required
def viewWatchlist(request):
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist_items = watchlist.listings.all()
    context = {'watchlist_items': watchlist_items}
    return render(request, 'auctions/watchlist.html', context)





@login_required
def bid(request, id):
    form = BidForm()
    pass

# @login_required
# def addComment(request, id):
#     form = CommentForm()
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.commenter = request.user
#             comment.auction_listing = AuctionListing.objects.get(id=id)
#             return redirect('listing', id=id)
#     return render(request, "auctions/createListing.html", {"form": form})

# @login_required
# def deleteComment(request, id):
#     comment = get_object_or_404(Comment, id=id)

#     if request.user == comment.commenter or request.user.has_perm('commerce.delete_comment'):
#         comment.delete()
    
#     # Redirect back to the listing page or another appropriate page
#     return redirect('listing', id=comment.auction_listing.id)

def addComment(request, id):
    currentUser = request.user
    listingData = AuctionListing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def deleteComment(request):
    pass



# @login_required
# def addComment(request, id):
#     form = CommentForm()
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.listing = AuctionListing.objects.get(id=id)
#             comment.save()
#             return redirect('listing', id=id)

#     # If the form is not valid, render the listing page with an error message
#     return render(request, "auctions/listing.html", {"form": form, "error_message": "Invalid form submission"})

# @login_required
# def deleteComment(request, id):
    comment = get_object_or_404(Comment, id=id)

    # Check if the current user is the commenter or has permission to delete any comment
    if request.user == comment.author or request.user.has_perm('commerce.delete_comment'):
        comment.delete()
        # Set a success message
        messages.success(request, "Comment deleted successfully.")
        return redirect('listing', id=comment.auction_listing.id)
    else:
        # Raise a PermissionDenied exception if the user doesn't have the right permissions
        raise PermissionDenied("You don't have permission to delete this comment.")