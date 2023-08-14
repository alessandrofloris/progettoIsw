from django.contrib import admin
from .models import User, Trip, Activity

# the following lines allow the admin users to modify 
# the app's models from the admin site.
admin.site.register(User)
admin.site.register(Trip)
admin.site.register(Activity)