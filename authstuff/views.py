from rest_framework import generics, permissions, views, status
from rest_framework.response import Response

from django.middleware.csrf import get_token

from .serializers import UserDetailsSerializer, UserDeleteSerializer


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CSRFView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'csrf_token': get_token(request)
        })


class UserDeleteView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        serializer = UserDeleteSerializer(data=request.data, context={
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        })
        serializer.is_valid(raise_exception=True)
        self.request.user.delete()
        return Response({"detail": "User deleted. (No takebacksies)."})
