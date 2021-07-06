from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{ self.name }"


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    image = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products', null=True)
    users = models.ManyToManyField(User, through='Cart')

    def __str__(self):
        return f"{ self.title }"

    def get_absolute_url(self):
        return reverse('products_detail', kwargs={'pk': self.pk})


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"CartID : { self.pk }"

    def get_absolute_url(self):
        return reverse('products_detail', kwargs={'pk': self.pk})
