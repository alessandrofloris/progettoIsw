from django.urls import path

from . import views

app_name = "travelGroup"
urlpatterns = [
    path("", views.index, name="index"),
    path("mytrips", views.trips),
    path("newtrip", views.newtrip),
    path("invite", views.invite),
    path("modifytrip/<int:trip_id>", views.modify_trip, name='modifytrip')
]