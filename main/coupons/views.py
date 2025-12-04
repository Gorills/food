from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from .models import Coupon
from .forms import CouponApplyForm
import logging

logger = logging.getLogger(__name__)


@require_POST
def coupon_apply(request):
    """
    Применение купона к сессии с улучшенной обработкой ошибок.
    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    
    # Получаем код купона с валидацией
    coupon_code = request.POST.get('coupon', '').strip()
    
    # Валидация: код купона обязателен
    if not coupon_code:
        logger.warning('Попытка применения пустого промокода')
        request.session['coupon_id'] = None
        messages.error(request, 'Необходимо указать промокод')
        return redirect('home')
    
    # Валидация: длина кода
    if len(coupon_code) > 50:
        logger.warning(f'Промокод слишком длинный: {len(coupon_code)} символов')
        request.session['coupon_id'] = None
        messages.error(request, 'Промокод слишком длинный')
        return redirect('home')
    
    try:
        # Поиск активного купона (case-insensitive, поддержка любых языков)
        # Используем Lower() для надежного поиска с кириллицей
        from django.db.models.functions import Lower
        
        coupon_code_lower = coupon_code.lower()
        
        coupon_obj = Coupon.objects.annotate(
            code_lower=Lower('code')
        ).filter(
            code_lower=coupon_code_lower,
            valid_from__lte=now,
            valid_to__gte=now,
            active=True
        ).first()
        
        if not coupon_obj:
            raise Coupon.DoesNotExist
        
        # Купон найден - сохраняем в сессию
        request.session['coupon_id'] = coupon_obj.id
        logger.info(f'Купон применен: {coupon_obj.code} (ID: {coupon_obj.id})')
        messages.success(request, f'Промокод {coupon_obj.code} успешно применен!')
        
    except Coupon.DoesNotExist:
        # Купон не найден
        logger.info(f'Купон не найден: {coupon_code}')
        request.session['coupon_id'] = None
        messages.error(request, 'Промокод не найден или недействителен')
        
    except Coupon.MultipleObjectsReturned:
        # Найдено несколько купонов (не должно быть)
        logger.error(f'Найдено несколько купонов с кодом: {coupon_code}')
        request.session['coupon_id'] = None
        messages.error(request, 'Ошибка в базе данных промокодов')
        
    except Exception as e:
        # Непредвиденная ошибка
        logger.error(f'Ошибка при применении купона {coupon_code}: {str(e)}')
        request.session['coupon_id'] = None
        messages.error(request, 'Ошибка при применении промокода')
    
    return redirect('home')