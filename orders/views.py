from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from notifications.tasks import send_order_notifications


class OrderListCreateView(generics.ListCreateAPIView):
    ''' List all orders or create a new order '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Only return orders for the logged-in customer
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(customer__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        customer = user.customerprofile
        order = serializer.save(customer=customer)
        send_order_notifications.delay(order.id)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    ''' Retrieve, update, or delete an order '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        ''' Only allow access to orders of the logged-in customer '''
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(customer__user=user)
