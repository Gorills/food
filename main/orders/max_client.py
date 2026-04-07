"""
Сервис мессенджера MAX (platform-api.max.ru), отдельно от Telegram.
Документация: https://dev.max.ru/docs-api/methods/POST/messages
"""
import logging
import re

import requests

logger = logging.getLogger(__name__)

MAX_API_BASE = 'https://platform-api.max.ru'


def telegram_md_v1_bold_to_max_markdown(text: str) -> str:
    """
    В шаблонах проекта для Telegram используется Markdown v1: *жирный*.
    В MAX для жирного нужен **текст** (см. раздел «Форматирование» в dev.max.ru/docs-api).
    Ссылки [текст](url) и моноширинный `код` в типичных случаях совпадают.
    """
    if not text:
        return ''
    return re.sub(r'\*([^*\n]+)\*', r'**\1**', text)


def resolve_max_chat_id(subdomain=None):
    """
    Как для Telegram-группы: субдомен (город) переопределяет значение по умолчанию из BaseSettings.
    """
    from setup.models import BaseSettings

    try:
        bs = BaseSettings.objects.get()
    except Exception:
        return None
    if subdomain and getattr(subdomain, 'max_chat_id', None) is not None:
        return subdomain.max_chat_id
    return getattr(bs, 'max_chat_id', None)


def resolve_max_chat_id_for_pickup_area(area):
    """Зона самовывоза (QR-меню): свой chat_id или дефолт из настроек."""
    from setup.models import BaseSettings

    try:
        bs = BaseSettings.objects.get()
    except Exception:
        return None
    if area and getattr(area, 'max_chat_id', None) is not None:
        return area.max_chat_id
    return getattr(bs, 'max_chat_id', None)


def send_max_message(access_token, chat_id, text, silent_fail=True, use_markdown=True):
    """
    POST /messages?chat_id=...
    При use_markdown=True в теле передаётся "format": "markdown" (официальное API MAX).
    """
    if not access_token or not str(access_token).strip():
        return False
    if chat_id is None:
        return False
    try:
        cid = int(chat_id)
    except (TypeError, ValueError):
        logger.warning('MAX: некорректный chat_id: %r', chat_id)
        if not silent_fail:
            raise ValueError('Некорректный MAX chat_id') from None
        return False

    url = f'{MAX_API_BASE}/messages'
    headers = {
        'Authorization': str(access_token).strip(),
        'Content-Type': 'application/json',
    }
    payload = {'text': (text or '')[:4000]}
    if use_markdown:
        payload['format'] = 'markdown'

    try:
        resp = requests.post(
            url,
            params={'chat_id': cid},
            headers=headers,
            json=payload,
            timeout=30,
        )
    except requests.RequestException as e:
        logger.warning('MAX: сеть: %s', e)
        if not silent_fail:
            raise
        return False

    if resp.status_code >= 400:
        logger.warning('MAX API %s: %s', resp.status_code, (resp.text or '')[:800])
        if not silent_fail:
            resp.raise_for_status()
        return False
    return True


def send_max_if_configured(chat_id, text_built_for_telegram_md_v1, silent_fail=True):
    """
    Отдельный канал уведомлений MAX: токен из BaseSettings, chat_id с маршрутизации.
    Текст приводится к разметке MAX (жирный **…**).
    """
    from setup.models import BaseSettings

    try:
        bs = BaseSettings.objects.get()
    except Exception:
        return False
    token = (getattr(bs, 'max_access_token', None) or '').strip()
    if not token or chat_id is None:
        return False
    max_text = telegram_md_v1_bold_to_max_markdown(text_built_for_telegram_md_v1)
    return send_max_message(token, chat_id, max_text, silent_fail=silent_fail, use_markdown=True)
