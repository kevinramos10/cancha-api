from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from gestion.serializers import UsuarioSerializer
from gestion.models import User

@api_view(['POST'])
def registro_usuario(request):

    serializer = UsuarioSerializer(data = request.data)

    if serializer.is_valid():

        datos = serializer.validated_data

        nuevoUsuario = User(
            nombre = datos.get('nombre'),
            email = datos.get('email'),
            telefono = datos.get('telefono')            
        )

        nuevoUsuario.set_password(datos.get('password'))
        nuevoUsuario.save()

        return Response(
            data={
                "message": "Usuario registrado exitosamente",
                "content": {
                    "id": str(nuevoUsuario.id),
                    "nombre": nuevoUsuario.nombre,
                    "email": nuevoUsuario.email
                }
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        data={
            "message": "Error al registrar el usuario",
            "content": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )