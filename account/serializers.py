from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_code, send_code2
from django.core.mail import send_mail

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=5, required=True)
    password_confirm = serializers.CharField(min_length=5, required=True)
    username = serializers.CharField(required=True)

    def validate_email(self,email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'A user with this email already exists'
            )
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password_confirm != password:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_code(user.email, user.activation_code)
        return user
    
    
class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(
                email=email,
                activation_code=code).exists():
            raise serializers.ValidationError(
                'User not found'
            )
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email
    
    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_code2(user.email, user.activation_code)
        return user


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=10, max_length=10, required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('User is not ')
        return code

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()