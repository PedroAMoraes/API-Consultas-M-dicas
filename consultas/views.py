from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status

from consultas.models import Consulta
from consultas.serializers import ConsultaSerializer

@api_view(['POST'])
def add_consulta(request):
    consulta = ConsultaSerializer(data = request.data)

    if Consulta.objects.filter(**request.data).exists():
        raise serializers.ValidationError('Dados existentes')

    if consulta.is_valid():
        consulta.save()
        return Response(consulta.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_all_consultas(request):
    if request.query_params:
        consultas = Consulta.objects.filter(**request.query_params.dict())
    else:
        consultas = Consulta.objects.all()

    if consultas:
        serializer = ConsultaSerializer(consultas, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_consulta(request, pk):
    consulta = Consulta.objects.get(pk=pk)
    data = ConsultaSerializer(instance= consulta, data= request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_consulta(request, pk):
    profissional = get_object_or_404(Consulta, pk=pk)
    profissional.delete()
    return Response(status=status.HTTP_202_ACCEPTED)