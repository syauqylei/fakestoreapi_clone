from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProductSerializer
from .models import Product
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(generics.CreateAPIView):
    query_set = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": f"User {username} has been created"}, status=status.HTTP_201_CREATED, headers=headers)


class ProductList(generics.ListAPIView):
    query_set = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
