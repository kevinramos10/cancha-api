from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from gestion.models import Tarifa
from gestion.serializers import TarifaSerializer

class TarifasView(APIView):

    def get(self, request: Request):
        tarifas = Tarifa.objects.filter(eliminado = False).all()

        serializer = TarifaSerializer(
            instance = tarifas,
            many = True
        )

        return Response(data={
            "content": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = TarifaSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data={
                "message": "Tarifa creada exitosamente",
                "content": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(data={
            "message": "Error al crear la tarifa",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TarifaView(APIView):
    def put(self, request: Request, id):

        id_existe = Tarifa.objects.filter(id = id, eliminado = False).first()

        if id_existe:
            serializer = TarifaSerializer(instance = id_existe, data = request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(data={
                    "message": "Tarifa actualizada exitosamente",
                    "content": serializer.data
                }, status=status.HTTP_200_OK)

            return Response(data={
                "message": "Error al actualizar la tarifa",
                "content": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={
            "message": "No se encontro la tarifa"
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, id):

        id_existe = Tarifa.objects.filter(id = id, eliminado = False).first()

        if id_existe:
            id_existe.eliminado = True
            id_existe.save()

            return Response(data=None, status=status.HTTP_204_NO_CONTENT)

        return Response(data={
            "message": "No se encontró la tarifa"
        }, status=status.HTTP_404_NOT_FOUND)