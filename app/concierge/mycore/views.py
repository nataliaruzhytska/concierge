from django.contrib.auth.decorators import permission_required, login_required
from django.core import serializers
from django.core.serializers import SerializerDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.generic import FormView, DetailView, ListView
from .forms import JournalForm, RoomForm, TenantForm
from .models import Tenant, Room, Journal


def health_check(request):
    return HttpResponse('OK')


def index(request):
    return HttpResponse(render_to_string('index.html', {'title': 'Concierge'}))


def created(request):
    return HttpResponse(render(request, template_name='created.html'))


def api_serializer_tenant(request, object_id):
    try:
        if object_id == 'all':
            tenants = Tenant.objects.all()
            return HttpResponse(serializers.serialize('json', tenants))
        else:
            tenant = Tenant.objects.filter(id=object_id)
            return HttpResponse(serializers.serialize('json', tenant))
    except (AttributeError, SerializerDoesNotExist, Tenant.DoesNotExist):
        return HttpResponse(status=404)


def api_serializer_room(request, object_id):
    try:
        if object_id == 'all':
            rooms = Room.objects.all()
            return HttpResponse(serializers.serialize('json', rooms))
        else:
            room = Room.objects.filter(id=object_id)
            return HttpResponse(serializers.serialize('json', room))
    except (AttributeError, SerializerDoesNotExist, Room.DoesNotExist):
        return HttpResponse(status=404)


def api_serializer_journal(request, object_id):
    try:
        if object_id == 'all':
            journals = Journal.objects.all()
            return HttpResponse(serializers.serialize('json', journals))
        else:
            journal = Journal.objects.filter(id=object_id)
            return HttpResponse(serializers.serialize('json', journal))
    except (AttributeError, SerializerDoesNotExist, Journal.DoesNotExist):
        return HttpResponse(status=404)


class TenantView(FormView):
    template_name = 'TenantForm.html'
    form_class = TenantForm
    success_url = 'created'

    def form_valid(self, form):
        form.save_tenant()
        return super().form_valid(form)


class RoomView(FormView):
    template_name = 'RoomForm.html'
    form_class = RoomForm
    success_url = 'created'

    def form_valid(self, form):
        form.save_room()
        return super().form_valid(form)


class JournalView(FormView):
    template_name = 'JournalForm.html'
    form_class = JournalForm
    success_url = 'created'

    def form_valid(self, form):
        form.save_journal()
        return super().form_valid(form)


class TenantListView(ListView):
    model = Tenant
    queryset = Tenant.objects.all()
    template_name = 'tenants_list.html'
    paginate_by = 10

    def get_all_tenants(self):
        return self.queryset


class RoomListView(ListView):
    model = Room
    queryset = Room.objects.all()
    template_name = 'rooms_list.html'
    paginate_by = 10

    def get_all_rooms(self):
        return self.queryset


class JournalListView(ListView):
    model = Journal
    queryset = Journal.objects.all()
    template_name = 'journals_list.html'
    paginate_by = 10

    def get_all_journals(self):
        return self.queryset


class TenantDetailView(DetailView):
    model = Tenant()
    queryset = Tenant.objects.all()
    template_name = 'tenant_detail.html'

    def get_tenant(self):
        return self.queryset.filter(tenant_id=self.kwargs.get('tenant_id'))


class RoomDetailView(DetailView):
    model = Room
    queryset = Room.objects.all()
    template_name = 'room_detail.html'

    def get_room(self):
        return self.queryset.filter(room_id=self.kwargs.get('room_id'))


class JournalDetailView(DetailView):
    model = Journal
    queryset = Journal.objects.all()
    template_name = 'journal_detail.html'

    def get_journal(self):
        return self.queryset.filter(journal_id=self.kwargs.get('journal_id'))


@login_required
@permission_required('mycore.change_journal')
def check_out(request, journal_id):
    journal = Journal.objects.get(id=journal_id)
    journal.key_out_date = timezone.now()
    journal.save_base()
    room = Room.objects.get(id=journal.room_id.id)
    room.is_free = True
    room.save_base()
    return render(request, 'check_out_form.html', {'key_out_date': journal.key_out_date})
