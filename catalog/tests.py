from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Product, Category


class ProductAPITests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="tester", password="pass1234")
        # Force authentication for all requests
        self.client.force_authenticate(user=self.user)

        # Create category
        self.category = Category.objects.create(name="Electronics")

        # Product payload
        self.product_data =[ {
            "name": "Test Laptop",
            "description": "A powerful test laptop",
            "price": "1999.99",
            "category": [self.category.name]
        }]

    def test_list_products(self):
        # Create a product first
        Product.objects.create(
            name="Phone",
            description="Test Phone",
            price="499.99",
            category=self.category
        )

        response = self.client.get("/api/catalog/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_product(self):
        # Ensure category exists
        self.assertTrue(Category.objects.filter(name="Electronics").exists())
        response = self.client.post("/api/catalog/products/upload/", self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, "Test Laptop")
