from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from .filters import ProfissionalFilter
from .models import Profissional
from .serializers import ProfissionalSerializer


@api_view(['POST'])
def add_profissional(request):
    profissional = ProfissionalSerializer(data= request.data)
    profissional.is_valid(raise_exception=True)
    profissional.save()
    return Response(profissional.data, status=status.HTTP_201_CREATED)


class ProfissionaisListView(ListAPIView):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfissionalFilter

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
def get_profissional(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    return Response(ProfissionalSerializer(profissional).data)


@api_view(['PUT'])
def update_profissional(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    serializer = ProfissionalSerializer(
        instance=profissional,
        data=request.data,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_profissional(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    try:
        profissional.delete()
    except ProtectedError:
        return Response(
            {'detail': 'Este profissional possui consultas vinculadas.'},
            status=status.HTTP_409_CONFLICT,
        )
    return Response(status=status.HTTP_202_ACCEPTED)
