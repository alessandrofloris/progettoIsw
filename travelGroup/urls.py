from django.urls import path

from . import views

app_name = "travelGroup"
urlpatterns = [
    path("mytrips", views.trips, name="mytrips"),
    path("newtrip", views.newtrip),
    path("modifytrip/<int:trip_id>", views.modify_trip, name='modifytrip'),
    path("", views.login_page, name='login'),
    path("registration", views.registration, name='signup'),
    path("logout", views.logout_page, name='logout'),
    path("invite", views.invite),
    path("viewtrip/<int:trip_id>", views.view_trip, name='viewtrip'),
]