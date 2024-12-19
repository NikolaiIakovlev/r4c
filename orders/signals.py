from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from orders.models import Order
from robots.models import Robot
from customers.models import Customer
from django.conf import settings


@receiver(post_save, sender=Robot)
def send_notification(sender, instance, created, **kwargs):
    if created == False and instance.in_stock and instance.in_stock == True:
        orders = Order.objects.filter(robot=instance, sent_notification=False)
        for order in orders:
            subject = f'Робот {instance.model}-{instance.version} теперь в наличии!'
            message = f'Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.'
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [Customer.objects.get(id=order.customer.id).email], fail_silently=False)
                order.sent_notification = True
                order.save()
            except Exception as e:
                print(f'Ошибка отправки email: {e}')
