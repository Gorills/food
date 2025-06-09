from django.core.management.base import BaseCommand
from django.utils import timezone
from integrations.iiko import load_menu
from shop.models import PickupAreas

class Command(BaseCommand):
    help = 'Синхронизация каталогов с IIKO'
    def handle(self, *args, **kwargs):
        unique_api_keys = PickupAreas.objects.filter(api_key__isnull=False).values_list('api_key', flat=True).distinct()
        

        if not unique_api_keys:
            load_menu(False, True, None)


        for api_key in unique_api_keys:
            area = PickupAreas.objects.filter(api_key=api_key).order_by('id').first()
            if area:
                load_menu(False, True, area)