from django.contrib import admin
from .models import FriendShip
# Register your models here.

@admin.register(FriendShip)
class FriendShipAdmin(admin.ModelAdmin):
    pass

