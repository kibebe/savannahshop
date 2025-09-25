from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from customers.models import CustomerProfile
from catalog.models import Category, Product
from orders.models import Order, OrderItem

class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="pass123")
        self.customer, _ = CustomerProfile.objects.get_or_create(
            user=self.user,
            defaults={"phone_number": "+254700000000"}
        )
        self.client.login(username="john", password="pass123")

        self.category = Category.objects.create(name="Phones")
        self.product = Product.objects.create(
            name="Samsung Galaxy S24",
            price=1200.00,
            category=self.category
        )

    def test_create_order(self):
        url = reverse("order-list-create")
        payload = {
            "items": [
                {"product": self.product.id, "quantity": 2}
            ]
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        order_item = OrderItem.objects.first()
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)

    def test_create_order_invalid_product(self):
        url = reverse("order-list-create")
        payload = {
            "items": [
                {"product": 9999, "quantity": 1}
            ]
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_unauthenticated(self):
        self.client.logout()
        url = reverse("order-list-create")
        payload = {
            "items": [
                {"product": self.product.id, "quantity": 1}
            ]
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Order.objects.count(), 0)