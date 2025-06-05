from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from app.core.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True, "allow_blank": False},
            "password": {
                "write_only": True,
                "required": True,
                "style": {"input_type": "password"},
            },
            "username": {
                "write_only": True,
                "required": True,
                "allow_blank": True,
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False, read_only=True)
    user_email = serializers.EmailField(
        source="user.email", write_only=True, required=True
    )

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["id"]
