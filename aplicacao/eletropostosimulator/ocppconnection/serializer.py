from rest_framework import serializers
from .models import Carregador

class CarregadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carregador
        fields = ['id_tag', 'status']
