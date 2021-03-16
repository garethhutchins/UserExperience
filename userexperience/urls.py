from django.urls import path
from userexperience import views

urlpatterns = [
    path("", views.home, name="home"),
    path("userexperience/<name>",views.hello_there,name="hello_there"),
    path("train/", views.train, name="train"),
    path("test/", views.test, name="test"),
    path("settings/", views.settings, name="settings"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]