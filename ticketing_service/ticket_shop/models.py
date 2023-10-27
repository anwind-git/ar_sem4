from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone


class PointsOfOriginAndDestination(models.Model):
    localities = models.CharField(max_length=100, verbose_name='Пункт отправления / прибытия')

    class Meta:
        db_table = 'points_of_origin_and_destination'
        verbose_name = 'пункт отправления / прибытия'
        verbose_name_plural = 'Пункты отправления / прибытия'
        ordering = ['localities']

    def __str__(self):
        return self.localities


class Day(models.Model):
    day_of_the_week = models.CharField(max_length=20, verbose_name='Дни недели')

    class Meta:
        db_table = 'day_of_the_week'
        verbose_name = 'день недели'
        verbose_name_plural = 'Дни недели'
        ordering = ['id']

    def __str__(self):
        return self.day_of_the_week


class Flight(models.Model):
    MODE_OF_TRANSPORTATION = (
        (0, '---------'),
        (1, 'Автобус'),
        (2, 'Mаршрутка'),
        (3, 'Поезд'),
        (4, 'Самолет')
    )
    category = models.IntegerField(choices=MODE_OF_TRANSPORTATION, default=0, verbose_name='Вид транспорта')
    shipping_point = models.ForeignKey(PointsOfOriginAndDestination, on_delete=models.PROTECT, related_name='destination_point', verbose_name='Пункт отправления')
    destination_point = models.ForeignKey(PointsOfOriginAndDestination, on_delete=models.PROTECT, related_name='shipping_point', verbose_name='Пункт назначения')
    intermediate_destinations = models.ManyToManyField(PointsOfOriginAndDestination, verbose_name='Промежуточные пункты назначения')
    transport = models.ForeignKey('Transport', on_delete=models.PROTECT, verbose_name='Транспорт')
    dispatcher_phone_number = models.CharField(max_length=20, verbose_name='Телефон диспетчера')
    departure_time = models.CharField(max_length=5, verbose_name='Время отправления')
    travel_time_hours = models.IntegerField(verbose_name='Время пути в часах')
    day_of_the_week = models.ManyToManyField(Day, verbose_name='Дни отправки')
    flight_status = models.BooleanField(default=False, verbose_name='Опубликован')

    class Meta:
        db_table = 'flight'
        verbose_name = 'рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['id']

    def __str__(self):
        return f'Рейс №{self.pk}'


class Transport(models.Model):
    transport_number = models.CharField(max_length=50, verbose_name='Регистрационный номер')
    number_of_seats = models.IntegerField(verbose_name='Количество посадочных мест')

    class Meta:
        db_table = 'transport'
        verbose_name = 'транспорт'
        verbose_name_plural = 'Транспорт'
        ordering = ['id']

    def __str__(self):
        return self.transport_number


class Client(models.Model):
    GENDR = (
        (0, '---------'),
        (1, 'М'),
        (2, 'Ж')
    )
    DOCUMENT = (
        (0, '---------'),
        (1, 'Паспорт РФ'),
        (2, 'Свидетельство о рождении РФ'),
        (3, 'Иностранный документ'),
        (4, 'Заграничный паспорт РФ'),
        (5, 'Военный билет'),
        (6, 'Паспорт моряка')
    )
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    telephone = models.CharField(unique=True, max_length=20, verbose_name='Телефон')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    document = models.IntegerField(choices=DOCUMENT, default=0, verbose_name='Тип документа')
    document_number = models.CharField(unique=True, max_length=50, verbose_name='Номер документа')
    gendr = models.IntegerField(choices=GENDR, default=0, verbose_name='Пол')
    Date_of_birth = models.DateField(verbose_name='Дата рождения')

    class Meta:
        db_table = 'customers'
        verbose_name = 'клиента'
        verbose_name_plural = 'Клиенты'
        ordering = ['id']

    def __str__(self):
        return self.last_name


class Tickets(models.Model):
    date_of_dispatch = models.DateField(verbose_name='Дата отправления')
    flight = models.ForeignKey('Flight', on_delete=models.PROTECT, verbose_name='Рейс')
    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Клиент')
    place = models.IntegerField(verbose_name='Мeсто')
    date_and_time_of_arrival = models.DateTimeField(blank=True, verbose_name='Дата и время прибытия')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость билета')

    class Meta:
        db_table = 'tickets'
        verbose_name = 'билет'
        verbose_name_plural = 'Билеты'
        ordering = ['-date_of_dispatch']

    def __str__(self):
        return f'Билет №{self.pk}'

    def save(self, *args, **kwargs):
        places = self.flight.transport.number_of_seats

        sold_tickets_count = Tickets.objects.filter(flight=self.flight, date_of_dispatch=self.date_of_dispatch).count()
        if sold_tickets_count >= places:
            raise ValidationError("Свободных мест на этом рейсе нет.")

        if Tickets.objects.filter(flight=self.flight, date_of_dispatch=self.date_of_dispatch,
                                  place=self.place).exists():
            raise ValidationError("Это место уже занято.")

        current_date = timezone.now().date()

        if self.date_of_dispatch < current_date:
            raise ValidationError("Нельзя купить билет на прошедшую дату.")

        current_day_of_week = General.get_day_of_week(self.date_of_dispatch)
        flight_days = [str(day) for day in self.flight.day_of_the_week.all()]
        print(current_day_of_week)
        print(flight_days)

        if str(current_day_of_week) not in flight_days:
            raise ValidationError("Нельзя купить билет на этот день недели.")

        departure_time = datetime.strptime(self.flight.departure_time, '%H:%M').time()

        departure_datetime = datetime.combine(self.date_of_dispatch, departure_time)
        arrival_datetime = departure_datetime + timedelta(hours=self.flight.travel_time_hours)
        self.date_and_time_of_arrival = arrival_datetime

        super().save(*args, **kwargs)


class General:
    def get_day_of_week(self):
        date_str = self.strftime('%Y-%m-%d')
        day_of_week = datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')
        return day_of_week