from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status

from consultas.models import Consulta
from consultas.serializers import ConsultaSerializer

@api_view(['POST'])
def add_consulta(request):
    consulta = ConsultaSerializer(data = request.data)


    consulta.is_valid(raise_exception=True)
    consulta.save()
    return Response(consulta.data, status=status.HTTP_201_CREATED)
   
    

@api_view(['GET'])
def get_all_consultas(request):
    filtros = serializers.Serializer(data=request.query_params)
    filtros.fields['profissional'] = serializers.IntegerField(required=False, min_value=1)
    filtros.is_valid(raise_exception=True)

    consultas = Consulta.objects.select_related('profissional').all()

    profissional_id = filtros.validated_data.get('profissional')
    if profissional_id is not None:
        consultas = consultas.filter(profissional_id=profissional_id)

    serializer = ConsultaSerializer(consultas, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def update_consulta(request, pk):
    consulta = Consulta.objects.get(pk=pk)
    data = ConsultaSerializer(instance= consulta, data= request.data)

    data.is_valid(raise_exception=True)
    data.save()
    return Response(data.data)
    
@api_view(['DELETE'])
def delete_consulta(request, pk):
    profissional = get_object_or_404(Consulta, pk=pk)
    profissional.delete()
    return Response(status=status.HTTP_202_ACCEPTED)