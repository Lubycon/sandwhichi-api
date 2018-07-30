from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from user.models import User, UserProfile

class SignupUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=2, max_length=30)
    has_terms = serializers.BooleanField(required=True)
    has_privacy_policy = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'has_terms', 'has_privacy_policy', )
        write_only_fields = ('password', )
        
    def validate_password(self, password):
        from django.contrib.auth import password_validation
        password_validation.validate_password(password)
        return password

    def validate_has_terms(self, has_terms):
        if has_terms != True:
            raise serializers.ValidationError()
        return has_terms
    
    def validate_has_privacy_policy(self, has_privacy_policy):
        if has_privacy_policy != True:
            raise serializers.ValidationError()
        return has_privacy_policy

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        return new_user


class SigninUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', )

    def validate_email(self, value):
        """
        해당 이메일을 가진 유저의 존재 여부 체크
        """
        email = value
        try:
            User.objects.get(email=email)
            pass
        except ObjectDoesNotExist:
            raise serializers.ValidationError('존재하지 않는 유저입니다. 이메일을 다시 한번 확인해주세요')

        return email


class MyUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('profile_image', 'abilities', 'keywords', 'is_certified_email', )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('profile_image', 'abilities', 'keywords', )


class MyUserSimpleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    profile_image = serializers.URLField()
    profile = MyUserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile',)


class UserSimpleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile', )


