from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from gestion.models import Reserva, HistorialReserva, Estado
from gestion.serializers import ReservaSerializer, CambiarEstadoReservaSerializer, HistorialReservaSerializer

class ReservasView(APIView):

    def get(self, request: Request):
        reservas = Reserva.objects.all()

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
            nuevaReserva = serializer.save()

            HistorialReserva.objects.create(
                reserva = nuevaReserva,
                estado_anterior = None,
                estado_nuevo = nuevaReserva.estado,
                motivo = "Reserva creada"
            )

            return Response(data={
                "message": "Reserva creada exitosamente",
                "content": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(data={
            "message": "Error al crear la Reserva",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ReservaView(APIView):

    def put(self, request: Request, id):
        id_existe = Reserva.objects.filter(id=id).first()

        if not id_existe:
            return Response(data={
                "message": "No se encontró la reserva"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CambiarEstadoReservaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                "message": "Error al actualizar la reserva",
                "content": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        estadoNuevo = serializer.validated_data.get("estado")
        motivo = serializer.validated_data.get("motivo")
        estadoAnterior = id_existe.estado

        if estadoAnterior in [Estado.CANCELADA, Estado.COMPLETADA]:
            return Response(data={
                "message": "La reserva ya se encuentra cancelada o completada"
            }, status=status.HTTP_400_BAD_REQUEST)

        if estadoNuevo == estadoAnterior:
            return Response(data={
                "message": "La reserva ya tiene ese estado"
            }, status=status.HTTP_400_BAD_REQUEST)

        id_existe.estado = estadoNuevo
        id_existe.save()

        HistorialReserva.objects.create(
            reserva = id_existe,
            estado_anterior = estadoAnterior,
            estado_nuevo = estadoNuevo,
            motivo = motivo
        )

        return Response(data={
            "message": "Reserva actualizada exitosamente",
            "content": ReservaSerializer(instance=id_existe).data
        }, status=status.HTTP_200_OK)


class HistorialReservaView(APIView):

    def get(self, request: Request, id):
        id_existe = Reserva.objects.filter(id=id).first()

        if not id_existe:
            return Response(data={
                "message": "No se encontró la reserva"
            }, status=status.HTTP_404_NOT_FOUND)

        historial = HistorialReserva.objects.filter(reserva = id_existe).order_by('created_at')

        serializer = HistorialReservaSerializer(
            instance = historial,
            many = True
        )

        return Response(data={
            "content": serializer.data
        }, status=status.HTTP_200_OK)
