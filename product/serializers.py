from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id title category price reviews'.split()


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, min_length=2)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(default=0)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category not found!')
        return category_id


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=3)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField(max_value=5, min_value=1)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product not found!')
        return product_id

