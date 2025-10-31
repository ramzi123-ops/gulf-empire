from django.urls import path
from apps.payments.views import payment_process, payment_success, payment_cancelled
from apps.payments.views.webhook_views import stripe_webhook

app_name = 'payments'

urlpatterns = [
    path('process/<int:order_id>/', payment_process, name='payment_process'),
    path('success/<int:order_id>/', payment_success, name='payment_success'),
    path('cancelled/', payment_cancelled, name='payment_cancelled'),
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
]
