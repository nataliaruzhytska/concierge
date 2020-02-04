from django import forms
from django.utils import timezone
from .models import Room, Tenant, Journal


class TenantForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    date_of_birth = forms.DateField()
    phone = forms.CharField()

    def save_tenant(self):
        tenant = Tenant(first_name=self.data['first_name'],
                        last_name=self.data['last_name'],
                        date_of_birth=self.data['date_of_birth'],
                        phone=self.data['phone'])
        tenant.save()


class RoomForm(forms.Form):
    number = forms.IntegerField()
    max_guests = forms.IntegerField()

    def save_room(self):
        room = Room(number=int(self.data['number']), max_guests=int(self.data['max_guests']))
        room.save()


class JournalForm(forms.Form):
    room_id = forms.IntegerField()
    tenant_id = forms.IntegerField()
    guests_count = forms.IntegerField()

    def save_journal(self):
        room = Room.objects.get(id=int(self.data['room_id']))
        tenant = Tenant.objects.get(id=int(self.data['tenant_id']))
        guests = int(self.data['guests_count'])
        journal = Journal(room_id=room, tenant_id=tenant, key_in_date=timezone.now(), guests_cnt=guests)
        journal.save()
