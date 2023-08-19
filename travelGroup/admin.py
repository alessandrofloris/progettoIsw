from django.contrib import admin
from .models import CustomUser, Trip, Activity, Invitation, Comment

# the following lines allow the admin users to modify 
# the app's models from the admin site.
admin.site.register(CustomUser)
admin.site.register(Trip)
admin.site.register(Activity)
admin.site.register(Invitation)
admin.site.register(Comment)
