from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .models import Category, Product, Review
from rest_framework import status


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        category_list = Category.objects.annotate(products_count=Count('products'))
        data = CategorySerializer(category_list, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category.id})


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category_detail = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error_message': 'Category not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategorySerializer(category_detail, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        category_detail.name = request.data.get('name')
        category_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category_detail.id})
    else:
        category_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        product_list = Product.objects.select_related('category').prefetch_related('reviews').all()
        data = ProductSerializer(product_list, many=True).data

        for product in data:
            reviews = product['reviews']
            if reviews:
                average_rating = sum(review['stars'] for review in reviews) / len(reviews)
            else:
                average_rating = 0
            product['average_rating'] = round(average_rating, 2)

        return Response(data=data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        return Response(status=status.HTTP_201_CREATED, data={'product_id': product.id})


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product_detail = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error_message': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product_detail, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        product_detail.title = request.data.get('title')
        product_detail.description = request.data.get('description')
        product_detail.price = request.data.get('price')
        product_detail.category_id = request.data.get('category_id')
        product_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'product_id': product_detail.id})
    else:
        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        review_list = Review.objects.all()
        data = ReviewSerializer(review_list, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')
        review = Review.objects.create(text=text, stars=stars, product_id=product_id)
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review.id})


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review_detail = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error_message': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review_detail, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        review_detail.text = request.data.get('text')
        review_detail.stars = request.data.get('stars')
        review_detail.product_id = request.data.get('product_id')
        review_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review_detail.id})
    else:
        review_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

