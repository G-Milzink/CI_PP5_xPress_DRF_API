from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile

# remove groups section from admin panel:
admin.site.unregister(Group)

# add profile section to admin panel:
admin.site.register(Profile)
