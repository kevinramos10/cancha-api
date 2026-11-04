from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from gestion.models import Cancha
from gestion.serializers import CanchaSerializer

class CanchasView(APIView):

    def get(self, request: Request):
        canchas = Cancha.objects.filter(eliminado = False).all()

        serializer = CanchaSerializer(
            instance = canchas,
            many = True
        )

        return Response(data={
            "content": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = CanchaSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data={
                "message": "Cancha creada exitosamente",
                "content": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(data={
            "message": "Error al crear la cancha",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CanchaView(APIView):

    def put(self, request: Request, id):
        id_existe = Cancha.objects.filter(id=id, eliminado=False).first()

        if not id_existe:
            return Response(data={
                "message": "No se encontró la cancha"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CanchaSerializer(instance=id_existe, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data={
                "message": "Cancha actualizada exitosamente",
                "content": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(data={
            "message": "Error al actualizar la cancha",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id):

        id_existe = Cancha.objects.filter(id = id, eliminado = False).first()

        if id_existe:
            id_existe.eliminado = True
            id_existe.save()

            return Response(data=None, status=status.HTTP_204_NO_CONTENT)

        return Response(data={
            "message": "No se encontró la cancha"
        }, status=status.HTTP_404_NOT_FOUND)
