from django.urls import path
from userexperience import views

urlpatterns = [
    path("", views.home, name="home"),
    path("train/", views.train, name="train"),
    path("test/", views.test, name="test"),
    path("settings/", views.settings, name="settings"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("results/", views.results, name="results"),
]