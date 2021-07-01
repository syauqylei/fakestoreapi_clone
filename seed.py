import requests
from myapi.models import Category, Product

# fetch categories
r = requests.get('https://fakestoreapi.com/products/categories')
categories = r.json()

for category in categories:
    data = Category(name=category)
    data.save()

fetchProducts = requests.get('https://fakestoreapi.com/products')
products = fetchProducts.json()

for product in products:
    print(product)
    item = Product(name=product['title'], content=product['description'])
    item.save()
