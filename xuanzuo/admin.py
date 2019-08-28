from django.contrib import admin

# Register your models here.
from .models import Metting

@admin.register(Metting)
class MettingAdmin():
    pass