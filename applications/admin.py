from django.contrib import admin

from .models import User, Application, Category, Place
admin.site.register(User)
admin.site.register(Application)
admin.site.register(Category)
admin.site.register(Place)

