from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.store.models import Sale
from apps.store.utils import create_recomendation


@receiver(m2m_changed, sender=Sale.products.through)
def m2m_changed_sale_products(sender, instance, action, **kwargs):
    if action == 'post_add':
        try:
            if not instance.products.all():
                return
            create_recomendation(instance)
        except Exception as e:
            print(f'Error creating recommendation: {e}')
            pass
