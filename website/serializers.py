from rest_framework import serializers, exceptions

from .models import MyUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['first_name', 'email', 'user_name', 'password', 'id']
        # password will not be render with the user
        extra_kwargs = {'password': {'write_only': True}}

    # override create method for password hashing
    def create(self, validated_data):
        user = MyUser(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
            first_name=validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user