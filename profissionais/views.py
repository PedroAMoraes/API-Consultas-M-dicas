from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status

from profissionais.models import Profissional
from profissionais.serializers import ProfissionalSerializer

@api_view(['POST'])
def add_profissional(request):
    profissional = ProfissionalSerializer(data = request.data)

    profissional.is_valid(raise_exception=True)
    profissional.save()
    return Response(profissional.data)

@api_view(['GET'])
def get_all_profissionais(request):
    if request.query_params:
        profissionais = Profissional.objects.filter(**request.query_params.dict())
    else:
        profissionais = Profissional.objects.all()

    if profissionais:
        serializer = ProfissionalSerializer(profissionais, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_profissional(request, pk):
    profissional = Profissional.objects.get(pk=pk)
    data = ProfissionalSerializer(instance= profissional, data= request.data)

    if data.is_valid(raise_exception=True):
        data.save()
        return Response(data.data)
    else:
        return Response(status= status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_profissional(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    profissional.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def my_test_500_view(request):
    # Return an "Internal Server Error" 500 response code.
    return Response(status=500)