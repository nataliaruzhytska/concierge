from django.db import models

# Create your models here.
from django.db.models import DO_NOTHING


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

    number = models.IntegerField(
        'Room number',

    )
    max_guests = models.IntegerField(
        'Maximum guests',

    )
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
        blank=True
    )
    tenant_id = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )
