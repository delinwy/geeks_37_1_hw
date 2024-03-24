from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .models import Category, Product, Review
from rest_framework import status


@api_view(['GET'])
def category_list_api_view(request):
    category_list = Category.objects.annotate(products_count=Count('products'))
    data = CategorySerializer(category_list, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category_detail = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error_message': 'Category not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategorySerializer(category_detail, many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
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


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product_detail = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error_message': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product_detail, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    review_list = Review.objects.all()
    data = ReviewSerializer(review_list, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review_detail = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error_message': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review_detail, many=False).data
    return Response(data=data)
