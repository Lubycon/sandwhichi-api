from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source='email',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(source='username')
    password = serializers.CharField(source='password')
    has_terms = serializers.BooleanField(source='has_terms')
    has_privacy_policy = serializers.BooleanField(source='has_privacy_policy')

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'has_terms', 'has_privacy_policy')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, user, validated_data):
        user.email = validated_data.get('email', user.email)
        user.username = validated_data.get('username', user.username)
        user.save()
        return user