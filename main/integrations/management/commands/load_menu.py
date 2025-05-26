from django.core.management.base import BaseCommand
from django.utils import timezone
from integrations.iiko import load_menu

class Command(BaseCommand):
    help = 'Синхронизация каталогов с IIKO'
    def handle(self, *args, **kwargs):
        load_menu(True, True, None)