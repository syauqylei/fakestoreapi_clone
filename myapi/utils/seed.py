import requests


def seed_data(apps, schema_editor):
    Product = apps.get_model('myapi', 'Product')
    Category = apps.get_model('myapi', 'Category')

    products = requests.get('https://fakestoreapi.com/products').json()
    categories = requests.get(
        'https://fakestoreapi.com/products/categories').json()

    for category in categories:
        createdCategory = Category.objects.create(name=category)
        createdCategory.save()

    for product in products:
        categoryId = Category.objects.all().filter(
            name=product['category']).get().id
        createdProduct = Product.objects.create(
            title=product['title'], price=product['price'], description=product['description'], image=product['image'], category_id=categoryId)

        createdProduct.save()
