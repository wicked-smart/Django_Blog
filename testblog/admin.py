from django.contrib import admin
from .models import *

# Register your models here.

for foo in [User, UserProfile, Tag, Blog, Comment]:
    admin.site.register(foo)
