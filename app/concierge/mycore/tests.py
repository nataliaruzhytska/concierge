import json
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError

from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from . import models
from .forms import TenantForm, RoomForm, JournalForm
from .settings import FIXTURES, CHECK_OUT_URL


class ViewTests(TestCase):

    def test_health_check(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_created_view(self):
        response = self.client.get(reverse('created'))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ConciergeViewTests(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        # Создание пользователя
        test_user = User.objects.create_user(username='testuser1', password='12345')
        test_user.save()
        permission1 = Permission.objects.get(codename='view_tenant')
        permission2 = Permission.objects.get(codename='view_room')
        permission3 = Permission.objects.get(codename='view_journal')
        test_user.user_permissions.add(permission1)
        test_user.user_permissions.add(permission2)
        test_user.user_permissions.add(permission3)
        test_user.save()
        login = self.client.login(username='testuser1', password='12345')

    def test_tenant_detail_view(self):
        response = self.client.get(reverse('tenant_detail', kwargs={'pk': 11}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_room_detail_view(self):
        response = self.client.get(reverse('room_detail', kwargs={'pk': 11}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_journal_detail_view(self):
        response = self.client.get(reverse('journal_detail', kwargs={"pk": 5}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tenant_list_view(self):
        response = self.client.get(reverse('tenant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)

    def test_room_list_view(self):
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)

    def test_journal_list_view(self):
        response = self.client.get(reverse('journal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)


class ApiTest(TestCase):
    fixtures = FIXTURES

    def test_api_tenant(self):
        test_tenant = [{"model": "mycore.tenant",
                        "pk": 11,
                        "fields": {
                            "first_name": "John",
                            "last_name": "Lennon",
                            "date_of_birth": "1990-11-20",
                            "phone": "123456789",
                            'photo': '',
                            'notes': None}
                        }]
        response = self.client.get(reverse('tenant_api', kwargs={'object_id': 11}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode("utf-8")), test_tenant)

    def test_api_room(self):
        test_room = [{"model": "mycore.room",
                      "pk": 13,
                      "fields": {
                          "number": 333,
                          "max_guests": 6,
                          "owner": None,
                          "is_free": True}
                      }]
        response = self.client.get(reverse('room_api', kwargs={'object_id': 13}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode("utf-8")), test_room)

    def test_api_journal(self):
        test_journal = [{"model": "mycore.journal",
                         "pk": 5,
                         "fields": {
                             "room_id": 12,
                             "guests_cnt": 1,
                             "key_in_date": "2020-01-05T17:57:23Z",
                             "key_out_date": "2020-01-05T18:05:09Z",
                             "tenant_id": 13,
                             "notes": ""
                         }
                         }]
        response = self.client.get(reverse('journal_api', kwargs={'object_id': 5}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.content.decode("utf-8")), test_journal)


class FormTests(TestCase):

    def test_tenant_form_valid(self):
        form = TenantForm(data={'first_name': 'AAA', 'last_name': 'BBB',
                                'date_of_birth': '2000-05-05', 'phone': '1234567'})
        self.assertTrue(form.is_valid())

    def test_tenant_form_invalid(self):
        form = TenantForm(data={'first_name': None, 'last_name': None,
                                'date_of_birth': '2000-05-05', 'phone': '1234567'})
        self.assertFalse(form.is_valid())

    def test_room_form_valid(self):
        form = RoomForm(data={'number': 15, 'max_guests': 2})
        self.assertTrue(form.is_valid())

    def _test_room_form_invalid(self):
        form = RoomForm(data={'number': 'qwerty', 'max_guests': '2'})
        self.assertFalse(form.is_valid())

    def test_journal_form_valid(self):
        form = JournalForm(data={'room_id': 11, 'tenant_id': 11, 'guests_count': 2,
                                 'key_in_date': '2020-01-05', 'key_out_date': None})
        self.assertTrue(form.is_valid())

    def test_journal_form_invalid(self):
        form = JournalForm(data={'room_id': 'z', 'tenant_id': '1', 'guests_count': '3',
                                 'key_in_date': '2020-01-05', 'key_out_date': None})
        self.assertFalse(form.is_valid())


class FormViewTests(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_user.save()
        permission1 = Permission.objects.get(codename='add_tenant')
        permission2 = Permission.objects.get(codename='add_room')
        permission3 = Permission.objects.get(codename='add_journal')
        test_user.user_permissions.add(permission1)
        test_user.user_permissions.add(permission2)
        test_user.user_permissions.add(permission3)
        test_user.save()
        login = self.client.login(username='testuser', password='12345')

    def test_tenant_form_view(self):
        tenant_count = models.Tenant.objects.count()
        response = self.client.post('/tenant/', data={'first_name': 'AAA', 'last_name': 'BBB',
                                                      'date_of_birth': '2000-05-05', 'phone': '1234567'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Tenant.objects.count(), tenant_count + 1)

    def test_room_form_view(self):
        room_count = models.Room.objects.count()
        response = self.client.post('/room/', data={'number': '55', 'max_guests': '2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Room.objects.count(), room_count + 1)

    def test_journal_form_view(self):
        journal_count = models.Journal.objects.count()
        response = self.client.post('/journal/', data={'room_id': '11', 'guests_count': '2',
                                                       'key_in_date': '2000-05-05', 'tenant_id': '11'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Journal.objects.count(), journal_count + 1)


class GetKeyTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_user.save()
        permission1 = Permission.objects.get(codename='add_journal')
        permission2 = Permission.objects.get(codename='change_journal')
        permission3 = Permission.objects.get(codename='change_room')
        test_user.user_permissions.add(permission1, permission2, permission3)
        login = self.client.login(username='testuser', password='12345')

    def test_get_room(self):
        free_room_count1 = models.Room.objects.filter(is_free=True).count()
        self.client.post('/journal/', data={'room_id': '12', 'guests_count': '2',
                                            'key_in_date': '2000-05-05', 'tenant_id': '11'})

        free_room_count2 = models.Room.objects.filter(is_free=True).count()
        self.assertEqual(free_room_count1 - 1, free_room_count2)

    def test_get_room_free(self):
        free_room_count1 = models.Room.objects.filter(is_free=True).count()
        self.client.post('/journal/', data={'room_id': '15', 'guests_count': '2',
                                            'key_in_date': '2019-07-05', 'tenant_id': '12'})

        free_room_count2 = models.Room.objects.filter(is_free=True).count()
        journal = models.Journal.objects.filter().latest('id')
        self.client.post(f'{CHECK_OUT_URL}{journal.id}/check_out_form')

        free_room_count3 = models.Room.objects.filter(is_free=True).count()
        self.assertEqual(free_room_count1 - 1, free_room_count2)
        self.assertEqual(free_room_count1, free_room_count3)

    def test_invalid_get_room(self):
        free_room_count1 = models.Room.objects.filter(is_free=True).count()
        self.client.post('/journal/', data={'room_id': '14', 'guests_count': '2',
                                            'key_in_date': '2019-07-05', 'tenant_id': '12'})
        free_room_count2 = models.Room.objects.filter(is_free=True).count()
        with self.assertRaises(ValidationError):
            self.client.post('/journal/', data={'room_id': '14', 'guests_count': '2',
                                                'key_in_date': '2019-07-05', 'tenant_id': '12'})
        free_room_count3 = models.Room.objects.filter(is_free=True).count()
        self.assertEqual(free_room_count1 - 1, free_room_count2)
        self.assertEqual(free_room_count2, free_room_count3)
