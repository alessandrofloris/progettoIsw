from django.urls import path

from . import views

app_name = "travelGroup"
urlpatterns = [
    path("", views.index, name="index"),
    path("mytrips", views.trips, name="mytrips"),
    path("newtrip", views.newtrip),
    path("modifytrip/<int:trip_id>", views.modify_trip, name='modifytrip'),
    path("login", views.login),
    path("registration", views.registration),
    path("invite", views.invite),
    path("viewtrip/<int:trip_id>", views.view_trip, name='viewtrip'),
]