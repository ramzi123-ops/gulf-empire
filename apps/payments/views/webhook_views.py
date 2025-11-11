from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
import stripe
import json
import logging

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.emails import (
    send_order_confirmation_email,
    send_payment_failed_email,
    send_refund_confirmation_email
)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Set up logging
logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Stripe webhook endpoint to handle payment events
    """
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    # Get the webhook secret from settings
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
    
    if not endpoint_secret:
        logger.error('Stripe webhook secret not configured')
        return HttpResponse('Webhook secret not configured', status=500)
    
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f'Invalid webhook payload: {str(e)}')
        return HttpResponse('Invalid payload', status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f'Invalid webhook signature: {str(e)}')
        return HttpResponse('Invalid signature', status=400)
    
    # Handle the event
    event_type = event['type']
    
    logger.info(f'Received Stripe webhook: {event_type}')
    
    # Handle payment intent succeeded event
    if event_type == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_succeeded(payment_intent)
    
    # Handle payment intent failed event
    elif event_type == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_failed(payment_intent)
    
    # Handle charge succeeded event (for additional tracking)
    elif event_type == 'charge.succeeded':
        charge = event['data']['object']
        handle_charge_succeeded(charge)
    
    # Handle charge refunded event
    elif event_type == 'charge.refunded':
        charge = event['data']['object']
        handle_charge_refunded(charge)
    
    else:
        logger.info(f'Unhandled event type: {event_type}')
    
    return JsonResponse({'status': 'success'})


def handle_payment_succeeded(payment_intent):
    """
    Handle successful payment intent
    """
    try:
        payment_intent_id = payment_intent['id']
        
        # Find the payment record
        payment = Payment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).first()
        
        if not payment:
            logger.error(f'Payment not found for intent: {payment_intent_id}')
            return
        
        # Update payment status
        payment.status = 'succeeded'
        payment.paid_at = timezone.now()
        payment.payment_method = payment_intent.get('payment_method_types', ['card'])[0]
        
        # Store charge ID if available
        if payment_intent.get('latest_charge'):
            payment.stripe_charge_id = payment_intent['latest_charge']
        
        payment.save()
        
        # Update order status
        order = payment.order
        order.payment_status = 'paid'
        order.status = 'confirmed'  # Move from pending to confirmed
        order.save()
        
        # CRITICAL: Deduct inventory for each order item
        for order_item in order.items.all():
            try:
                inventory = order_item.product.inventory
                success = inventory.remove_stock(order_item.quantity)
                if not success:
                    # Critical error - insufficient inventory after payment!
                    logger.critical(
                        f'INVENTORY MISMATCH: Failed to deduct {order_item.quantity} units '
                        f'of {order_item.product.sku} for Order #{order.order_number}. '
                        f'Current stock: {inventory.quantity}'
                    )
                else:
                    logger.info(
                        f'Deducted {order_item.quantity} units of {order_item.product.sku}. '
                        f'Remaining: {inventory.quantity}'
                    )
            except Exception as e:
                # Log but don't fail the payment - inventory issue needs manual resolution
                logger.error(
                    f'Error deducting inventory for {order_item.product.sku}: {str(e)}'
                )
        
        logger.info(f'Payment succeeded for Order #{order.order_number}')
        
        # Send confirmation email to customer
        send_order_confirmation_email(order)
        
    except Exception as e:
        logger.error(f'Error handling payment succeeded: {str(e)}')


def handle_payment_failed(payment_intent):
    """
    Handle failed payment intent
    """
    try:
        payment_intent_id = payment_intent['id']
        
        # Find the payment record
        payment = Payment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).first()
        
        if not payment:
            logger.error(f'Payment not found for intent: {payment_intent_id}')
            return
        
        # Update payment status
        payment.status = 'failed'
        
        # Store error message
        error = payment_intent.get('last_payment_error', {})
        if error:
            payment.error_message = error.get('message', 'Payment failed')
        
        payment.save()
        
        # Update order status
        order = payment.order
        order.payment_status = 'failed'
        order.save()
        
        logger.warning(f'Payment failed for Order #{order.order_number}')
        
        # Send payment failed notification
        send_payment_failed_email(order)
        
    except Exception as e:
        logger.error(f'Error handling payment failed: {str(e)}')


def handle_charge_succeeded(charge):
    """
    Handle successful charge (additional tracking)
    """
    try:
        payment_intent_id = charge.get('payment_intent')
        
        if not payment_intent_id:
            return
        
        # Find the payment record
        payment = Payment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).first()
        
        if payment:
            payment.stripe_charge_id = charge['id']
            payment.save()
            
            logger.info(f'Charge succeeded: {charge["id"]}')
        
    except Exception as e:
        logger.error(f'Error handling charge succeeded: {str(e)}')


def handle_charge_refunded(charge):
    """
    Handle refunded charge
    """
    try:
        payment_intent_id = charge.get('payment_intent')
        
        if not payment_intent_id:
            return
        
        # Find the payment record
        payment = Payment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).first()
        
        if not payment:
            logger.error(f'Payment not found for intent: {payment_intent_id}')
            return
        
        # Update payment status
        payment.status = 'refunded'
        payment.save()
        
        # Update order status
        order = payment.order
        order.payment_status = 'refunded'
        order.status = 'cancelled'
        order.save()
        
        # CRITICAL: Restore inventory for each order item
        for order_item in order.items.all():
            try:
                inventory = order_item.product.inventory
                success = inventory.add_stock(order_item.quantity)
                if success:
                    logger.info(
                        f'Restored {order_item.quantity} units of {order_item.product.sku}. '
                        f'New stock: {inventory.quantity}'
                    )
                else:
                    logger.error(
                        f'Failed to restore {order_item.quantity} units of {order_item.product.sku}'
                    )
            except Exception as e:
                logger.error(
                    f'Error restoring inventory for {order_item.product.sku}: {str(e)}'
                )
        
        logger.info(f'Charge refunded for Order #{order.order_number}')
        
        # Send refund confirmation email
        send_refund_confirmation_email(order)
        
    except Exception as e:
        logger.error(f'Error handling charge refunded: {str(e)}')
