import random

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserLoginSerializer, UserConfirmationSerializer
from django.contrib.auth import authenticate, login
from .models import UserConfirmation
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data, is_active=False)
    confirmation = UserConfirmation.objects.create(user=user, code=random.randint(100000, 999999))
    return Response({'status': 'User registered', 'code': confirmation.code, 'data': serializer.data},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
def confirm_user_api_view(request):
    serializer = UserConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data.get('code')
    confirmation = get_object_or_404(UserConfirmation, code=code)
    user = confirmation.user
    user.is_active = True
    user.save()
    confirmation.delete()
    return Response({'status': 'User activated'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    login(request, user)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        user.save()
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
