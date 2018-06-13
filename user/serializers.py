from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import User

class SignupUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=2, max_length=30)
    has_terms = serializers.BooleanField(required=True)
    has_privacy_policy = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'has_terms', 'has_privacy_policy', )
        write_only_fields = ('password', )

    def __init__(self, *args, **kwargs):
        super(SignupUserSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_password(self, password):
        from django.contrib.auth import password_validation
        password_validation.validate_password(password)

        return password

    def validate_has_terms(self, has_terms):
        if has_terms != True:
            raise serializers.ValidationError("이용 약관에 동의해주세요")
        return has_terms
    
    def validate_has_privacy_policy(self, has_privacy_policy):
        if has_privacy_policy != True:
            raise serializers.ValidationError("개인정보보호정책에 동의해주세요")
        return has_privacy_policy

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)

        return new_user
    