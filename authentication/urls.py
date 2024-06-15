from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_agency_user/", views.registerAgencyUser, name="register_agency_user"),
    path("register_client_user/", views.registerClientUser, name="register_client_user"),
    path("login_agency_user/", views.login_agency_user, name="login_agency_user"),
    path("login_client_user/", views.login_client_user, name="login_client_user"),
    path("get_current_agency_user/", views.get_current_agency_user, name="get_current_agency_user"),
    path("get_current_client_user/", views.get_current_client_user, name="get_current_client_user"),
]