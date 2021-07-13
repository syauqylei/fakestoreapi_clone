from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProductSerializer
from .models import Product
from rest_framework import generics, status, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsStaffPermission
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from django.shortcuts import redirect


def RedirectViewSwagger(request):
    return redirect('schema-swagger-ui')


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


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsStaffPermission]
    serializer_class = ProductSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': f"Product {serializer.data['title']} has been created"}, status=status.HTTP_201_CREATED)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    lookup_url_kwargs = 'product_id'

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return Product.objects.filter(pk=product_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        if len(serializer.data):
            [response] = serializer.data
        else:
            raise NotFound('The product is not found',
                           code='product_not_found')

        return Response(response, status=status.HTTP_200_OK)
