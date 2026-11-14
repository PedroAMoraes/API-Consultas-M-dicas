import django_filters

from .models import Profissional

class ProfissionalFilter(django_filters.FilterSet):
    
    nome_social = django_filters.CharFilter(
        field_name= 'nome_social',
        lookup_expr='icontains',
    )
    profissao = django_filters.CharFilter(
        field_name='profissao',
        lookup_expr='icontains',
    )



    class Meta:
        model = Profissional
        fields = ['nome_social', 'profissao']

        