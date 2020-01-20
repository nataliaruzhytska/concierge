import requests
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from . import models
from .forms import TenantForm, RoomForm, JournalForm
from .settings import FIXTURES, API_URL


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


class SerializerTests(TestCase):

    fixtures = FIXTURES

    def test_api_serializer_tenant(self):
        response = requests.get(f'{API_URL}tenant/all')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_api_serializer_room(self):
        response = requests.get(f'{API_URL}room/all')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_api_serializer_journal(self):
        response = requests.get(f'{API_URL}journal/all')
        self.assertEqual(response.status_code, HTTPStatus.OK)


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
