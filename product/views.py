from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer
from .models import Category, Product, Review
from rest_framework import status


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        category_list = Category.objects.annotate(products_count=Count('products'))
        data = CategorySerializer(category_list, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        name = serializer.validated_data.get('name')
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
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_detail.name = serializer.validated_data.get('name')
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
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
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
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_detail.title = serializer.validated_data.get('title')
        product_detail.description = serializer.validated_data.get('description')
        product_detail.price = serializer.validated_data.get('price')
        product_detail.category_id = serializer.validated_data.get('category_id')
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
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')
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
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review_detail.text = serializer.validated_data.get('text')
        review_detail.stars = serializer.validated_data.get('stars')
        review_detail.product_id = serializer.validated_data.get('product_id')
        review_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review_detail.id})
    else:
        review_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

