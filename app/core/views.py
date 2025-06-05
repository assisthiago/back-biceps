from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.core.models import Student
from app.core.permissions import AllowAnyToCreate
from app.core.serializers import StudentSerializer, UserSerializer
from app.shortcuts import get_list_or_404, get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAnyToCreate]

    def get_queryset(self):
        return get_list_or_404(User, id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(User, id=kwargs.get("pk"))
        return Response(data=self.get_serializer(obj).data, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAnyToCreate]

    def get_queryset(self):
        return get_list_or_404(Student, user__id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, email=serializer.validated_data.get("user").get("email")
        )

        obj, created = Student.objects.get_or_create(user=user)
        return Response(
            data=self.get_serializer(obj).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(Student, id=kwargs.get("pk"))
        return Response(data=self.get_serializer(obj).data, status=200)
