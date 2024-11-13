import datetime
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from .serializers import RegistrationSerializer

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegistrationView(APIView):
    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        request_body=RegistrationSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Successful authorisation",
                examples={
                    "application/json": {
                        "refresh": "some_refresh_token_here",
                        "access": "some_access_token_here"
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: 'Bad request'
        }
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
