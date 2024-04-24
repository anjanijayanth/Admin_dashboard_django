"""admin_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login_view, name='login'),
    path('home',views.dashboard, name='home'),
    path('',views.my_view),
    path('logout/',views.logout_view, name='logout'),
    path('staff/',views.staff_detail, name='staff_detail'),
    path('org_details/',views.org_detail, name='org_detail'),
    path('agent_logs/',views.agent_logs, name='agent_logs'),
    path('agency_detail/',views.agency_detail, name='agency_detail'),
    path('agent_detail/',views.agent_detail, name='agent_detail'),
    path('update/<str:pk>/',views.update_or_create_org, name='org_update'),
    path('create/',views.update_or_create_org, name='org_create'),
    path('agent-log-search/', views.partial_search_logs, name='partial_search_logs'),
    path('agency-search/', views.agency_search, name='agency_search'),
    path('agent-search/', views.agent_search, name='agent_search'),
    path('staff-search/', views.staff_search, name='staff_search'),
]



handler404 = 'user.views.custom_page_not_found_view'
handler500 = 'user.views.custom_error_view'
handler403 = 'user.views.custom_permission_denied_view'