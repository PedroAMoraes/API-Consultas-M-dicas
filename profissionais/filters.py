import django_filters

from .models import Profissional

class ProfissionalFilter(django_filters.FilterSet):
    
    nome = django_filters.CharFilter(
        field_name= 'nome',
        lookup_expr='icontains',
    )
    profissao = django_filters.CharFilter(
        field_name='profissao',
        lookup_expr='icontains',
    )



    class Meta:
        model = Profissional
        fields = ['nome', 'profissao']

        