"""concierge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import path, include
from django.views.decorators.cache import cache_page

from .settings import CACHE_TTL
from .views import health_check, index, JournalView, created, RoomView, TenantView, TenantDetailView, RoomDetailView, \
    JournalDetailView, TenantListView, RoomListView, JournalListView, api_serializer_tenant, api_serializer_room, \
    api_serializer_journal, check_out

static_patterns = static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT) + \
                  static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug:slug>/accounts/', include('django.contrib.auth.urls')),
    path('healthcheck/', health_check, name='health_check'),
    path('', index, name='index'),
    path('journal/', permission_required('mycore.add_journal', 'mycore.change_journal')(JournalView.as_view()), name='add_journal'),
    path('room/', permission_required('mycore.add_room')(RoomView.as_view()), name='add_room'),
    path('tenant/', permission_required('mycore.add_tenant')(TenantView.as_view()), name='add_tenant'),
    path('journal/created/', created, name='created'),
    path('room/created/', created, name='created'),
    path('tenant/created/', created, name='created'),
    path('tenants/', login_required(TenantListView.as_view()), name='tenant_list'),
    path('rooms/', login_required(RoomListView.as_view()), name='room_list'),
    path('journals/', JournalListView.as_view(), name='journal_list'),
    path('tenants/tenant_detail/<pk>/', cache_page(CACHE_TTL)(TenantDetailView.as_view()), name='tenant_detail'),
    path('journals/journal_detail/<pk>/', JournalDetailView.as_view(), name='journal_detail'),
    path('journals/journal_detail/<journal_id>/check_out_form', check_out, name='check_out'),
    path('rooms/room_detail/<pk>/', cache_page(CACHE_TTL)(RoomDetailView.as_view()), name='room_detail'),
    path('api/tenant/<object_id>/', api_serializer_tenant, name='tenant_api'),
    path('api/room/<object_id>/', api_serializer_room, name='room_api'),
    path('api/journal/<object_id>/', cache_page(CACHE_TTL)(api_serializer_journal), name='journal_api')
] + static_patterns
