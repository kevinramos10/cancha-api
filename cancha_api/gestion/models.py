from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.contrib.auth.models import UserManager

class ManejadorUsuario(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields["rol"] = "ADMIN"

        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True)

    nombre = models.CharField(max_length=50, null=False)

    email = models.EmailField(unique=True, null=False)

    telefono = models.CharField(max_length=20, null=False)

    class Rol(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        ADMIN = 'ADMIN', 'Administrador'

    rol = models.CharField(
        max_length=10,
        choices = Rol.choices,
        default = Rol.CLIENTE
    )

    habilitado = models.BooleanField(default=True)

    eliminado = models.BooleanField(default=False)

    objects = ManejadorUsuario()

    class Meta:
        db_table = 'users'


class Cliente(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True)

    apodo = models.CharField(
        max_length=30,
        unique=True,
        null=False,
    )

    habilitado = models.BooleanField(default=True)
    
    eliminado = models.BooleanField(default=False)

    #Relacion
    user = models.OneToOneField(
        to=User,
        on_delete=models.PROTECT,
        db_column='user_id'
    )

    class Meta:
        db_table = 'clientes'

class Sede(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True)

    nombre = models.CharField(max_length=50, null=False)

    direccion = models.CharField(max_length=50, null=False)

    ciudad = models.CharField(max_length=50, null=False)

    habilitado = models.BooleanField(default=True)

    eliminado = models.BooleanField(default=False)

    class Meta:
        db_table = 'sedes'

class Media(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    ext = models.CharField(max_length=100, null=False)
    ruta = models.CharField(max_length=200, null=False)
    mimeType = models.CharField(db_column='mime_type', max_length=100, null=False)
    habilitado = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)

    class Meta:
        db_table = 'medias'

class Cancha(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True)

    nombre = models.CharField(max_length=50, null=False)

    class Tipo(models.TextChoices):
        F5 = 'FUTBOL 5', 'Futbol 5'
        F6 = 'FUTBOL 6', 'Futbol 6'
        F7 = 'FUTBOL 7', 'Futbol 7'
        F11 = 'FUTBOL 11', 'Futbol 11'

    tipo = models.CharField(max_length=20, choices=Tipo.choices, null=False)

    habilitado = models.BooleanField(default=True)
        
    eliminado = models.BooleanField(default=False)

    #Relacion
    sede = models.ForeignKey(
        to=Sede,
        on_delete=models.PROTECT,
        db_column='sede_id'
    )

    media = models.OneToOneField(
        to=Media,
        on_delete=models.PROTECT,
        db_column='media_id',
        null=True
    )

    class Meta:
        db_table = 'canchas'



class Tarifa(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    hora_inicio = models.TimeField(null=False)

    hora_fin = models.TimeField(null=False)

    precio_hora = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    habilitado = models.BooleanField(default=True)
        
    eliminado = models.BooleanField(default=False)

    #Relacion
    cancha = models.ForeignKey(
        to=Cancha,
        on_delete=models.PROTECT,
        db_column='cancha_id'
    )

    class Meta:
        db_table = 'tarifas'

class Estado(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    CONFIRMADA = 'CONFIRMADA', 'Confirmada'
    CANCELADA = 'CANCELADA', 'Cancelada'
    COMPLETADA = 'COMPLETADA', 'Completada'

class Reserva(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    fecha_inicio = models.DateTimeField(null=False)

    fecha_fin = models.DateTimeField(null=False)

    estado = models.CharField(max_length=20, choices=Estado.choices, null=False)

    precio_total = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    #Relacion
    cliente = models.ForeignKey(
        to=Cliente, 
        on_delete=models.PROTECT,
        db_column='cliente_id'
    )

    cancha = models.ForeignKey(
        to=Cancha,
        on_delete=models.PROTECT,
        db_column='cancha_id'
    )

    class Meta:
        db_table = 'reservas'

class HistorialReserva(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True)

    estado_anterior = models.CharField(max_length=20, choices=Estado.choices, null=True, blank=True)

    estado_nuevo = models.CharField(max_length=20, choices=Estado.choices, null=False)

    motivo = models.CharField(max_length=50, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    #Relacion
    reserva = models.ForeignKey(
        to=Reserva,
        on_delete=models.PROTECT,
        db_column='reserva_id'
    )

    class Meta:
        db_table = 'historial_reservas'


