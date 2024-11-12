from rest_framework import serializers
from .models import Carregador
  
class CarregadorSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Carregador
        fields = ['id_tag', 'status', 'status_display']

