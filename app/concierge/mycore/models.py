from django.core.exceptions import ValidationError
from django.db import models


class Tenant(models.Model):
    """
    Room's owner/tenant
    """
    first_name = models.CharField(
        'First name',
        max_length=250,
    )
    last_name = models.CharField(
        'Last name',
        max_length=250,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        db_index=True,
    )
    phone = models.CharField(
        'Phone num',
        max_length=20,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        'Photo',
        upload_to='tenant',
        help_text='Photo of the tenant',
        null=True,
        blank=True
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class Room(models.Model):
    """
    model Room
    """

    number = models.IntegerField('Room number')
    max_guests = models.IntegerField('Maximum guests')
    owner = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_free = models.BooleanField(
        'is free',
        default=True
    )

    class Meta:
        ordering = ['number']


class Journal(models.Model):
    """
    model Journal
    """
    room_id = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )
    guests_cnt = models.IntegerField(
        'Count guests',

    )
    key_in_date = models.DateTimeField(
        'Date and time check-in',
        db_index=True
    )
    key_out_date = models.DateTimeField(
        'Date and time check-out',
        db_index=True,
        null=True,
        blank=True,
    )
    tenant_id = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['id']

    @property
    def key_transfer(self):
        return f'{self.room_id}, {self.key_in_date}, {self.key_out_date}, {self.guests_cnt}, {self.tenant_id}'

    def __str__(self):
        return self.key_transfer

    def save(self, *args, **kwargs):
        room = self.room_id
        if self.key_out_date:
            if room.is_free is False:
                room.is_free = True
                room.owner = None
                room.save()
                super().save(*args, **kwargs)
        else:
            if self.guests_cnt > room.max_guests:
                raise ValidationError(f"Maximum available {room.max_guests} guests")
            else:
                if room.is_free is True:
                    room.is_free = False
                    room.owner = self.tenant_id
                    room.save()
                    super().save(*args, **kwargs)
                else:
                    raise ValidationError(f"This room isn't free. Please, choose another")
