from typing import __all__

from rest_framework import serializers

from profissionais.models import Profissional
from profissionais.serializers import ProfissionalSerializer
from .models import Consulta


class ConsultaSerializer(serializers.ModelSerializer):

    info_profissional = ProfissionalSerializer(source='profissional', read_only=True)
    
    id_profissional = serializers.PrimaryKeyRelatedField(
        queryset=Profissional.objects.all(),
        write_only=True
    )

    class Meta:
        model = Consulta
        fields = ('id','data','id_profissional','info_profissional')