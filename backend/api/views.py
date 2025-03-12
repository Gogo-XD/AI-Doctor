# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import PatientSerializer, DoctorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class CreatePatientView(generics.CreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

class CreateDoctorView(generics.CreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        is_doctor = request.user.groups.filter(name='Doctor').exists()
        is_patient = request.user.groups.filter(name='Patient').exists()

        data = {
            "username": request.user.username,
            "role": "doctor" if is_doctor else "patient" if is_patient else "unknown",
            # Additional data here...
        }
        return Response(data)



