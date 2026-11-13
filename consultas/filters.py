import django_filters

from .models import Consulta

class ConsultaFilter(django_filters.FilterSet):
    
    data = django_filters.IsoDateTimeFilter(field_name='data')
    profissional = django_filters.NumberFilter(field_name='profissional_id')

    nome_profissional = django_filters.CharFilter(
        field_name='profissional__nome',
        lookup_expr='icontains',
    )
    profissao_profissional = django_filters.CharFilter(
        field_name='profissional__profissao',
        lookup_expr='icontains',
    )
    contato_profissional = django_filters.CharFilter(
        field_name='profissional__contato',
        lookup_expr='icontains',
    )


    class Meta:
        model = Consulta
        fields = []

        