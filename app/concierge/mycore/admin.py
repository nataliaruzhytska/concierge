# Register your models here.
from django.conf import settings
from django.contrib import admin

from .models import Tenant, Room, Journal


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'phone')
    search_fields = ('first_name', 'last_name', 'phone', 'date_of_birth')
    list_filter = ('date_of_birth', 'last_name')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'max_guests', 'owner', 'is_free')
    search_fields = ('number', 'max_guests', 'owner', 'is_free')
    list_filter = ('number', 'owner', 'is_free')




@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'guests_cnt', 'key_in_date', 'key_out_date', 'tenant_id')
    search_fields = ('room_id', 'key_in_date', 'key_out_date', 'tenant_id')
    list_filter = ('room_id', 'key_in_date', 'key_out_date', 'tenant_id')
