from celery import shared_task
from orders.models import Order
from django.core.mail import send_mail
import africastalking
from django.conf import settings

@shared_task
def send_order_notifications(order_id):
    order = Order.objects.select_related('customer__user').prefetch_related('items__product').get(pk=order_id)
    customer = order.customer
    user = customer.user
    print("we got here")

    # Set AT_USERNAME and AT_API_KEY in env
    try:
        africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
        sms = africastalking.SMS
        message = f"Hi {user.first_name or user.username}, your order #{order.id} was received."
        # sandbox: use AT_SANDBOX= True in configuration if required
        response = sms.send(message, [customer.phone_number])
    except Exception as e:
        # log error
        print("SMS error:", e)

    # -- Email
    try:
        subject = f"New order #{order.id}"
        body = f"Order {order.id} by {user.get_full_name() or user.username}\nItems:\n"
        for item in order.items.all():
            body += f"- {item.product.name} x {item.quantity} (price={item.product.price})\n"
        admin_email = settings.ADMIN_EMAIL
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [admin_email])
    except Exception as e:
        print("Email error:", e)
