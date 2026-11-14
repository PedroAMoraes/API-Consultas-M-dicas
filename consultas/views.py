from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from .filters import ConsultaFilter
from .models import Consulta
from .serializers import ConsultaSerializer


@api_view(['POST'])
def add_consulta(request):
    consulta = ConsultaSerializer(data=request.data)
    consulta.is_valid(raise_exception=True)
    consulta.save()
    return Response(consulta.data, status=status.HTTP_201_CREATED)


class ConsultaslListView(ListAPIView):
    queryset = Consulta.objects.select_related('profissional')
    serializer_class = ConsultaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConsultaFilter

    def filter_queryset(self, queryset):
        allowed = set(self.filterset_class.base_filters)
        if api_settings.URL_FORMAT_OVERRIDE:
            allowed.add(api_settings.URL_FORMAT_OVERRIDE)

        unknown = set(self.request.query_params.keys()) - allowed
        if unknown:
            raise ValidationError({
                'query_params': (
                    f"Filtro(s) inválido(s): {', '.join(sorted(unknown))}"
                )
            })

        return super().filter_queryset(queryset)


@api_view(['GET'])
def get_consulta(request, pk):
    consulta = get_object_or_404(
        Consulta.objects.select_related('profissional'),
        pk=pk,
    )
    return Response(ConsultaSerializer(consulta).data)


@api_view(['PUT'])
def update_consulta(request, pk):
    consulta = get_object_or_404(
        Consulta.objects.select_related('profissional'),
        pk=pk,
    )
    serializer = ConsultaSerializer(instance=consulta, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.delete()
    return Response(status=status.HTTP_202_ACCEPTED)