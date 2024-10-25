from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .serializers import RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    """
    View for registering a new user and obtaining JWT tokens.
    """

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegistrationSerializer,
        description="Register a new user and obtain JWT tokens.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        return Response(
            {
                "access": access_token,
                "refresh": refresh_token,
            },
            status=status.HTTP_201_CREATED,
        )
