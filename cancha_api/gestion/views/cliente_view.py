from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from gestion.serializers import ClienteSerializer
from gestion.models import Cliente

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from gestion.permissions import EsAdmin


class ClienteView(APIView):

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsAuthenticated()]

        return [IsAuthenticated(), EsAdmin()]

    def get(self, request: Request):
        clientes = Cliente.objects.filter(eliminado = False).all()

        serializer = ClienteSerializer(
            instance = clientes,
            many = True
        )

        return Response(data={
            "content": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = ClienteSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)

            return Response(
                data={
                    "message": "Cliente registrado correctamente",
                    "content": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            data={
                "message": "Error al registrar el cliente",
                "content": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request: Request, id):
        cliente = Cliente.objects.filter(id=id, eliminado=False).first()

        if not cliente:
            return Response(data={
                "message": "Cliente no enconetrado"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ClienteSerializer(instance=cliente, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data={
                    "message": "Cliente actualizado correctamente",
                    "content": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            data={
                "message": "Error al actualizar el cliente",
                "content": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, id):
        cliente = Cliente.objects.filter(
            id=id,
            eliminado=False
        ).first()

        if not cliente:
            return Response(
                data={
                    "message": "Cliente no encontrado"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cliente.eliminado = True
        cliente.save()

        return Response(
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )
