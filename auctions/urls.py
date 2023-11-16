from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("edit/<int:id>", views.editListing, name="edit"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path('add-watchlist/<int:id>', views.addToWatchlist, name="addToWatchlist"),
    path('delete-watchlist/<int:id>', views.deleteFromWatchlist, name="deleteFromWatchlist"),
    path('watchlist', views.viewWatchlist, name="watchlist"),
    path('addcomment/<int:id>', views.addComment, name="addComment"),
    path('deleteComment/<int:id>', views.deleteComment, name="deleteComment")
]
