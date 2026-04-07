"""
Список групповых чатов бота по официальному API (GET /chats).
Используйте chat_id из ответа в настройках — не число из ссылки в браузере, если они различаются.

https://dev.max.ru/docs-api/methods/GET/chats
"""
import json

import requests
from django.core.management.base import BaseCommand

from orders.max_client import MAX_API_BASE
from setup.models import BaseSettings


class Command(BaseCommand):
    help = 'Показать групповые чаты MAX для токена из BaseSettings (max_access_token)'

    def handle(self, *args, **options):
        try:
            bs = BaseSettings.objects.get()
        except BaseSettings.DoesNotExist:
            self.stderr.write(self.style.ERROR('BaseSettings не найдены'))
            return

        token = (bs.max_access_token or '').strip()
        if not token:
            self.stderr.write(self.style.ERROR('В настройках сайта не задан max_access_token'))
            return

        url = f'{MAX_API_BASE}/chats'
        headers = {'Authorization': token}
        try:
            r = requests.get(url, headers=headers, params={'count': 100}, timeout=30)
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Запрос не удался: {e}'))
            return

        self.stdout.write(f'HTTP {r.status_code}\n')
        try:
            data = r.json()
            self.stdout.write(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception:
            self.stdout.write(r.text)

        self.stdout.write(
            '\nПодставьте в админке поле «MAX: id чата» значение chat_id из нужного чата '
            '(бот должен быть участником группы; статус в ответе — active).'
        )
