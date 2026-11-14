from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from gestion.models import Reserva
from gestion.serializers import ReservaSerializer

class ReservasView(APIView):

    def get(self, request: Request):
        reservas = Reserva.objects.filter(eliminado = False).all()

        serializer = ReservaSerializer(
            instance = reservas,
            many = True
        )

        return Response(data={
            "content": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = ReservaSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data={
                "message": "Reserva creada exitosamente",
                "content": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(data={
            "message": "Error al crear la Reserva",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    