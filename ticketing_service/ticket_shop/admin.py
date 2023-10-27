from django.contrib import admin
from .models import PointsOfOriginAndDestination, Flight, Transport, Client, Tickets, Day
from django.utils.html import format_html


@admin.register(PointsOfOriginAndDestination)
class PointsOfOriginAndDestinationAdmin(admin.ModelAdmin):
    list_display = ['localities']
    search_fields = ['localities']
    list_per_page = 15


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'transport', 'shipping_point', 'departure_time', 'destination_point', 'flight_status', 'create_ticket_button']
    filter_horizontal = ['intermediate_destinations', 'day_of_the_week']
    list_editable = ['flight_status']
    search_fields = ['pk', 'transport__transport_number']
    list_per_page = 15

    def create_ticket_button(self, obj):
        return format_html(f'<a href="/admin/ticket_shop/tickets/add/?flight={obj.pk}" class="button"">Продать билет</a>', obj.pk)
    create_ticket_button.short_description = 'Продать билет'


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ['transport_number', 'number_of_seats']
    list_per_page = 15


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'document',  'telephone']
    earch_fields = ['last_name', 'first_name', 'middle_name', 'document',  'telephone', 'email']
    list_per_page = 15


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ['flight', 'place', 'date_of_dispatch', 'flight_departure_time', 'date_and_time_of_arrival']
    readonly_fields = ['date_and_time_of_arrival']
    list_per_page = 15

    def flight_departure_time(self, obj):
        return obj.flight.departure_time

    flight_departure_time.short_description = 'Время отправления'


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ['day_of_the_week']
