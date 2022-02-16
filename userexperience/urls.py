from django.urls import path
from userexperience import views

urlpatterns = [
    path("", views.home, name="home"),
    path("train/", views.train, name="train"),
    path("settings/", views.settings, name="settings"),
    path("about/", views.about, name="about"),
    path("results/", views.results, name="results"),
    path("manage/", views.manage, name="manage"),
    
]