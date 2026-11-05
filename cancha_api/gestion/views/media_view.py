import os

from uuid import uuid4
from urllib.parse import unquote

from boto3 import client

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from gestion.serializers import GenerarUrlAWSSerializer

class GenerarUrlAWSView(APIView):

    def post(self, request: Response):

        serializer = GenerarUrlAWSSerializer(data = request.data)

        if serializer.is_valid():

            fileName = serializer.validated_data.get("fileName")
            ext = serializer.validated_data.get("ext")
            contentType = serializer.validated_data.get("contentType")
            folder = serializer.validated_data.get("folder", "medias/")

            s3 = client('s3')

            nombre = str(uuid4()) + '_' + fileName

            url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    "Bucket": os.getenv('BUCKET_NAME'),
                    "Key": folder + nombre + '.' + ext,
                    "ContentType": contentType
                },
                ExpiresIn=150
            )

            return Response(data={
                "content": {
                    "url": unquote(url),
                    "nombre": nombre,
                    "ext": ext,
                    "mimeType": contentType,
                    "ruta": folder
                }
            }, status=status.HTTP_200_OK)

        else:
            return Response(data={
                "message": "Error al generar URL",
                "content": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


