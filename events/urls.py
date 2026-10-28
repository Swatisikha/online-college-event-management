from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'register/<int:event_id>/',
        views.register_event,
        name='register_event'
    ),

    path('signup/', views.signup, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path(
        'my-registrations/',
        views.my_registrations,
        name='my_registrations'
    ),
    path(
        'dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),
    path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
]