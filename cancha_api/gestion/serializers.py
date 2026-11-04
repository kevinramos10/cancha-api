from rest_framework import serializers
from .models import Sede, Cancha


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = '__all__'