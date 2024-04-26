from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.authentication import TokenAuthentication

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes=[TokenAuthentication]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            is_admin = serializer.validated_data.get('is_admin', False)
            is_staff = serializer.validated_data.get('is_staff', False)
            if is_admin:
                serializer.save(is_admin=is_admin, is_staff=True)
            elif is_staff:
                serializer.save(is_staff=is_staff)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)