from rest_framework import serializers
from .models import Sede, Cancha, Media, Tarifa, User, Cliente

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




