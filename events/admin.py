from django.contrib import admin
from .models import Event, Registration


# -----------------------------
# Event Management
# -----------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'date',
        'venue',
        'registration_deadline',
        'max_participants',
    )    
    list_display_links=('title',)


    search_fields = (
        'title',
        'description',
        'venue',
    )

    list_filter = (
        'date',
        'venue',
        'registration_deadline',
    )

    ordering = ('date', 'title')
    date_hierarchy = 'date'
    list_per_page = 10


# -----------------------------
# Registration Management
# -----------------------------
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student_name',
        'email',
        'phone_number',
        'college_roll_number',
        'event',
    )

    list_display_links = ('student_name',)

    search_fields = (
        'student__username',
        'student_name',
        'email',
        'phone_number',
        'college_roll_number',
        'event__title',
    )

    list_filter = ('event',)

    ordering = ('student_name',)

    list_per_page = 10

    list_select_related = ('event',)