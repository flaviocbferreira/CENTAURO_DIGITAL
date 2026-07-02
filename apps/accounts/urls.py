from django.urls import path

from .views import AccountLoginView, AccountLogoutView, LogoutConfirmView

app_name = "accounts"

urlpatterns = [
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", LogoutConfirmView.as_view(), name="logout"),
    path("logout/confirm/", AccountLogoutView.as_view(), name="logout_confirm"),
]
