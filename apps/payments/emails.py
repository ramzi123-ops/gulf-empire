"""
Email notifications for payment events
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order):
    """Send order confirmation email to customer after successful payment"""
    try:
        subject = f'تأكيد الطلب #{order.order_number} - إمبراطور الخليج'
        
        # Render HTML email template
        html_message = render_to_string('payments/emails/order_confirmation.html', {
            'order': order,
            'user': order.user,
        })
        
        # Plain text fallback
        plain_message = f"""
        شكراً لطلبك من إمبراطور الخليج!
        
        رقم الطلب: {order.order_number}
        المبلغ الإجمالي: {order.total_price} ر.س
        حالة الدفع: مدفوع
        
        سيتم معالجة طلبك قريباً.
        
        مع تحيات،
        فريق إمبراطور الخليج
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f'Order confirmation email sent to {order.user.email} for order {order.order_number}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send order confirmation email for order {order.order_number}: {str(e)}')
        return False


def send_payment_failed_email(order):
    """Send payment failed notification to customer"""
    try:
        subject = f'فشل الدفع للطلب #{order.order_number}'
        
        plain_message = f"""
        عذراً، فشلت عملية الدفع للطلب #{order.order_number}.
        
        يمكنك المحاولة مرة أخرى من خلال حسابك.
        
        إذا استمرت المشكلة، يرجى التواصل معنا.
        
        مع تحيات،
        فريق إمبراطور الخليج
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        
        logger.info(f'Payment failed email sent to {order.user.email} for order {order.order_number}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send payment failed email for order {order.order_number}: {str(e)}')
        return False


def send_refund_confirmation_email(order):
    """Send refund confirmation email to customer"""
    try:
        subject = f'تأكيد استرداد المبلغ للطلب #{order.order_number}'
        
        plain_message = f"""
        تم استرداد مبلغ الطلب #{order.order_number} بنجاح.
        
        المبلغ: {order.total_price} ر.س
        
        سيظهر المبلغ في حسابك البنكي خلال 5-10 أيام عمل.
        
        مع تحيات،
        فريق إمبراطور الخليج
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        
        logger.info(f'Refund confirmation email sent to {order.user.email} for order {order.order_number}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send refund email for order {order.order_number}: {str(e)}')
        return False
