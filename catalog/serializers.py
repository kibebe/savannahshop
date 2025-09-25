from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    average_price_url = serializers.HyperlinkedIdentityField(
        view_name='category-average-price',
        lookup_field='pk'
    )
    class Meta:
        model = Category
        fields = ['id','name','parent', 'average_price_url']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_detail', 'created_at']
