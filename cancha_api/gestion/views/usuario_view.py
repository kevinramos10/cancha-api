from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from gestion.serializers import UsuarioSerializer
from gestion.models import User

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from gestion.serializers import LoginSerializare

from rest_framework.permissions import IsAuthenticated

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


@api_view(['POST'])
def login_usuario(request):

    serializer = LoginSerializare(data = request.data)

    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        usuario = authenticate(
            request,
            email = email,
            password = password
        )

        if usuario is not None:
            refresh = RefreshToken.for_user(usuario)
            access = refresh.access_token

            return Response(data={
                "message": "Inicio de session exitoso",
                "content": {
                    "refresh": str(refresh),
                    "acces": str(access)
                }
            }, status=status.HTTP_200_OK)        
        else:
            return Response(data={
                "message": "Correo o password incorrectos",                
            }, status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response(data={
            "message": "Error al iniciar sesion",
            "content": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def perfilUsuario(request):

    usuarioActual = request.user
    serializador = UsuarioSerializer(instance = usuarioActual)
    return Response(data={
        "content": serializador.data
    })
