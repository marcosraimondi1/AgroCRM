from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newLand", views.newLand, name="newLand"),
    path("profile", views.profile, name="profile"),
    path("billing", views.billing_view, name="billing"),
    path("editLand/<int:land_id>", views.editLand, name="editLand"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API ROUTES
    path("land/<int:land_id>", views.land, name="land"),
    path("messages", views.messages, name="messages"),
]
