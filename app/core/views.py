from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from app.core.permissions import AllowAnyToCreate
from app.core.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAnyToCreate]

    def get_queryset(self):
        return get_list_or_404(User, id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get("pk"))
        return Response(data=self.get_serializer(user).data, status=200)
