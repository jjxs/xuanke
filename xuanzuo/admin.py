from django.contrib import admin

# Register your models here.
from .models import Metting, UserMetting, User

admin.site.register(Metting)
admin.site.register(UserMetting)
admin.site.register(User)