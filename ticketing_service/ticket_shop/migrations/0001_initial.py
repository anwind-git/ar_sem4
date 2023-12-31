# Generated by Django 4.2.6 on 2023-10-27 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=50, verbose_name='Отчество')),
                ('telephone', models.CharField(max_length=20, unique=True, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('document', models.IntegerField(choices=[(0, '---------'), (1, 'Паспорт РФ'), (2, 'Свидетельство о рождении РФ'), (3, 'Иностранный документ'), (4, 'Заграничный паспорт РФ'), (5, 'Военный билет'), (6, 'Паспорт моряка')], default=0, verbose_name='Тип документа')),
                ('document_number', models.CharField(max_length=50, unique=True, verbose_name='Номер документа')),
                ('gendr', models.IntegerField(choices=[(0, '---------'), (1, 'М'), (2, 'Ж')], default=0, verbose_name='Пол')),
                ('Date_of_birth', models.DateField(verbose_name='Дата рождения')),
            ],
            options={
                'verbose_name': 'клиента',
                'verbose_name_plural': 'Клиенты',
                'db_table': 'customers',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_the_week', models.CharField(max_length=20, verbose_name='Дни недели')),
            ],
            options={
                'verbose_name': 'день недели',
                'verbose_name_plural': 'Дни недели',
                'db_table': 'day_of_the_week',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(0, '---------'), (1, 'Автобус'), (2, 'Mаршрутка'), (3, 'Поезд'), (4, 'Самолет')], default=0, verbose_name='Вид транспорта')),
                ('dispatcher_phone_number', models.CharField(max_length=20, verbose_name='Телефон диспетчера')),
                ('departure_time', models.CharField(max_length=5, verbose_name='Время отправления')),
                ('travel_time_hours', models.IntegerField(verbose_name='Время пути в часах')),
                ('flight_status', models.BooleanField(default=False, verbose_name='Опубликован')),
                ('day_of_the_week', models.ManyToManyField(to='ticket_shop.day', verbose_name='Дни отправки')),
            ],
            options={
                'verbose_name': 'рейс',
                'verbose_name_plural': 'Рейсы',
                'db_table': 'flight',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PointsOfOriginAndDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localities', models.CharField(max_length=100, verbose_name='Пункт отправления / прибытия')),
            ],
            options={
                'verbose_name': 'пункт отправления / прибытия',
                'verbose_name_plural': 'Пункты отправления / прибытия',
                'db_table': 'points_of_origin_and_destination',
                'ordering': ['localities'],
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_number', models.CharField(max_length=50, verbose_name='Регистрационный номер')),
                ('number_of_seats', models.IntegerField(verbose_name='Количество посадочных мест')),
            ],
            options={
                'verbose_name': 'транспорт',
                'verbose_name_plural': 'Транспорт',
                'db_table': 'transport',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_dispatch', models.DateField(verbose_name='Дата отправления')),
                ('place', models.IntegerField(verbose_name='Мeсто')),
                ('date_and_time_of_arrival', models.DateTimeField(blank=True, verbose_name='Дата и время прибытия')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Стоимость билета')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticket_shop.client', verbose_name='Клиент')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticket_shop.flight', verbose_name='Рейс')),
            ],
            options={
                'verbose_name': 'билет',
                'verbose_name_plural': 'Билеты',
                'db_table': 'tickets',
                'ordering': ['-date_of_dispatch'],
            },
        ),
        migrations.AddField(
            model_name='flight',
            name='destination_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shipping_point', to='ticket_shop.pointsoforiginanddestination', verbose_name='Пункт назначения'),
        ),
        migrations.AddField(
            model_name='flight',
            name='intermediate_destinations',
            field=models.ManyToManyField(to='ticket_shop.pointsoforiginanddestination', verbose_name='Промежуточные пункты назначения'),
        ),
        migrations.AddField(
            model_name='flight',
            name='shipping_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_point', to='ticket_shop.pointsoforiginanddestination', verbose_name='Пункт отправления'),
        ),
        migrations.AddField(
            model_name='flight',
            name='transport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticket_shop.transport', verbose_name='Транспорт'),
        ),
    ]
