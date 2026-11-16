from rest_framework import serializers
from .models import Sede, Cancha, Media, Tarifa, User, Cliente, Reserva, HistorialReserva
from decimal import Decimal

#Sede
class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

#Cancha
class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = '__all__'

#Media
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

#Gerador URL para Media
class GenerarUrlAWSSerializer(serializers.Serializer):

    extensionesValidas = ["png", "jpg", "jpeg", "pdf"]

    contentTypeValidas = [
        "image/jpeg",
        "image/png",
        "application/pdf"
    ]

    fileName = serializers.CharField(
        trim_whitespace=True,
        max_length=100,
        required=True
    )

    ext = serializers.ChoiceField(
        choices=extensionesValidas,
        required=True
    )

    contentType = serializers.ChoiceField(
        choices = contentTypeValidas,
        required = True
    )

    size = serializers.FloatField(
        max_value=10*1024*1024,
        min_value=5*1024,
        required=True
    )

    folder = serializers.CharField(required=False)

#Tarifa
class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'

#usuarios
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        exclude = [
            'is_staff',
            'is_superuser',
            'is_active',
            'user_permissions',
            'last_login',
            'groups',
            'rol'

        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

from django.utils import timezone
from rest_framework import serializers
from datetime import time
from zoneinfo import ZoneInfo
from gestion.models import Estado

class ReservaSerializer(serializers.ModelSerializer):

    def validate_fecha_inicio(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "La fecha inicio debe ser posterior a la fecha actual"
            )
        return value

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if fecha_fin <= fecha_inicio:
            raise serializers.ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio"
            )

        duracion = fecha_fin - fecha_inicio
        if duracion.total_seconds() < 3600:
            raise serializers.ValidationError(
                "La reserva debe tener una duracion minima de 1 hora"
            )

        if duracion.total_seconds() > 10800:
            raise serializers.ValidationError(
                "La reserva no puede tener una duración mayor a 3 horas"
            )

        hora_apertura = time(8, 0)
        hora_cierre = time(23, 0)

        fecha_inicio_lima = timezone.localtime(fecha_inicio, ZoneInfo("America/Lima"))
        fecha_fin_lima = timezone.localtime(fecha_fin, ZoneInfo("America/Lima"))

        if fecha_inicio_lima.date() != fecha_fin_lima.date():
            raise serializers.ValidationError(
                "La reserva debe comenzar y terminar el mismo día"
            )

        if fecha_inicio_lima.time() <  hora_apertura or fecha_fin_lima.time() > hora_cierre:
            raise serializers.ValidationError(
                "Las reservas deben estar dentro del horario de atencion (8:00 a 23:00)"
            )

        cancha = data.get('cancha')

        reserva_existente = Reserva.objects.filter(
            cancha = cancha,
            fecha_inicio__lt = fecha_fin,
            fecha_fin__gt = fecha_inicio,
            estado__in=[
                Estado.PENDIENTE,
                Estado.CONFIRMADA,
            ]
        )
        if reserva_existente.exists():
            raise serializers.ValidationError(
                "La cancha ya tiene una reserva en ese horario"
            )

        if not cancha.habilitado or cancha.eliminado:
            raise serializers.ValidationError(
                "La cancha no se encuentra disponible para reservas"
            )

        sede = cancha.sede

        if not sede.habilitado or sede.eliminado:
            raise serializers.ValidationError(
                "La sede no se encuentra disponible para reservas"
            )

        cliente = data.get('cliente')

        if not cliente.habilitado or cliente.eliminado:
            raise serializers.ValidationError(
            "El cliente no se encuentra habilitado para realizar reservas"
            )

        tarifas = Tarifa.objects.filter(
            cancha=cancha,
            habilitado=True,
            eliminado=False
        ).order_by('hora_inicio')
        if not tarifas.exists():
            raise serializers.ValidationError(
                "La cancha no tiene tarifas disponibles"
            )

        tarifa = tarifas.filter(
            hora_inicio__lte = fecha_inicio_lima.time(),
            hora_fin__gte = fecha_fin_lima.time()
        ).first()
        if not tarifa:
            raise serializers.ValidationError(
                "No hay una tarifa que cubra el horario de la reserva"
            )

        horas = Decimal(duracion.total_seconds()) / Decimal(3600)

        data['precio_total'] = tarifa.precio_hora * horas
        data['estado'] = Estado.PENDIENTE

        return data

    class Meta:
        model = Reserva
        fields = '__all__'
        extra_kwargs = {
            'estado': {'read_only': True},
            'precio_total': {'read_only': True}
        }

#Cambiar estado de Reserva
class CambiarEstadoReservaSerializer(serializers.Serializer):

    estado = serializers.ChoiceField(
        choices = Estado.choices,
        required = True
    )

    motivo = serializers.CharField(
        trim_whitespace=True,
        max_length=50,
        required=True
    )

#HistorialReserva
class HistorialReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialReserva
        fields = '__all__'


