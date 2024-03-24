from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return f'Review for {self.product.title}'
