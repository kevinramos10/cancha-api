from rest_framework import serializers
from .models import Sede, Cancha, Media

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


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