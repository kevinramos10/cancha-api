from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from gestion.models import Sede
from gestion.serializers import SedeSerializer


class SedesView(APIView):

    def get(self, request: Request):
        sedes = Sede.objects.filter(eliminado = False).all()

        serializer = SedeSerializer(
            instance = sedes,
            many = True
        )

        return Response(data={
            "content": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = SedeSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data={
                "message": "Sede creada exitosamente",
                "content": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(data={
            "message": "Error al crear la sede",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SedeView(APIView):

    def put(self, request: Request, id):

        id_existe = Sede.objects.filter(id = id, eliminado = False).first()

        if id_existe:

            serializer = SedeSerializer(instance=id_existe, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(data={
                    "message": "Sede actualizada exitosamente",
                    "content": serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response(data={
                "message": "Error al actualizar la sede",
                "content": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(data={
            "message": "Error al actualizar la sede",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id):

        id_existe = Sede.objects.filter(id = id, eliminado = False).first()

        if id_existe:
            id_existe.eliminado = True
            id_existe.save()

            return Response(data=None, status=status.HTTP_204_NO_CONTENT)

        return Response(data={
            "message": "No se encontró la sede"
        }, status=status.HTTP_404_NOT_FOUND)

    




