from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ProductSerializer, CategorySerializer
from .models import Category, Product
from .utils import category_ids, get_or_create_category_by_path
from django.db.models import Avg
from rest_framework import generics


class ProductUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Accept JSON array of products with fields:
        """
        items = request.data
        created = []
        for item in items:
            cat = get_or_create_category_by_path(item.get('category', []))
            category = Category.objects.filter(name=cat).first() if cat else None
            serializer = ProductSerializer(data={
                'name': item['name'],
                'description': item.get('description',''),
                'price': item['price'],
                'category': category.id
            },
            context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            created.append(serializer.data)
        return Response(created, status=status.HTTP_201_CREATED)


class CategoryAveragePriceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        ids = category_ids(category)
        avg = Product.objects.filter(category__in=ids).aggregate(avg_price=Avg('price'))['avg_price'] or 0
        return Response({'category_id': pk, 'average_price': avg})


class ProductListView(generics.ListAPIView):
    """
    GET /api/catalog/products/ → list all products
    """
    queryset = Product.objects.all().select_related("category")
    serializer_class = ProductSerializer
