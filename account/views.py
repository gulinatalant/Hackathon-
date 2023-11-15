from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully, register! Please, Verify your email address!',status=200)
    

class ActivationView(APIView):
    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response(
            'Email address successfully verifed!, Thank you!', status=200
        )
    
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам выслан код для восстановления пароля')
        


class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно обновлен')
 