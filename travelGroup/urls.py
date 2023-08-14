from django.urls import path

from . import views

app_name = "travelGroup"
urlpatterns = [
    path("", views.index, name="index"),
    path("mytrips", views.trips),
]