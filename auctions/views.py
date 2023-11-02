from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Comment, User, AuctionListing, Watchlist
from .forms import AuctionForm, CommentForm


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

def listing(request, auction_id):
    listing = AuctionListing.objects.get(id=auction_id)
    # watchlist,created = Watchlist.objects.get_or_create(user=request.user)
    # is_in_watchlist = listing in watchlist.listings.all()
    is_in_watchlist = request.user.watchlist.listings.all()
    context = {'listing': listing, "is_in_watchlist": is_in_watchlist}
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
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist_items = watchlist.listings.all()
    context = {'watchlist_items': watchlist_items}
    return render(request, 'auctions/watchlist.html', context)

@login_required
def bid(request):
    pass

@login_required
def addComment(request, id):
    form = CommentForm()
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commenter = request.user
            comment.auction_listing = AuctionListing.objects.get(id=id)
            return redirect('listing', id=id)
    return render(request, "auctions/createListing.html", {"form": form})

@login_required
def deleteComment(request, id):
    comment = get_object_or_404(Comment, id=id)

    if request.user == comment.commenter or request.user.has_perm('commerce.delete_comment'):
        comment.delete()
    
    # Redirect back to the listing page or another appropriate page
    return redirect('listing', id=comment.auction_listing.id)