from django.contrib import admin
from .models import Coupon, CouponUsageLog


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'promo_type', 'valid_from', 'valid_to', 'active', 'current_uses', 'max_uses']
    list_filter = ['active', 'promo_type', 'valid_from', 'valid_to']
    search_fields = ['code', 'slug']
    prepopulated_fields = {'slug': ('code',)}
    date_hierarchy = 'valid_from'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'slug', 'discount', 'promo_type', 'active')
        }),
        ('Период действия', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Ограничения использования', {
            'fields': ('max_uses', 'current_uses'),
            'description': 'Настройки ограничения количества использований'
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'current_uses']


@admin.register(CouponUsageLog)
class CouponUsageLogAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user_phone', 'discount_amount', 'order_total', 'success', 'used_at']
    list_filter = ['success', 'used_at', 'coupon']
    search_fields = ['coupon__code', 'user_phone', 'user_ip', 'order_id']
    date_hierarchy = 'used_at'
    ordering = ['-used_at']
    
    fieldsets = (
        ('Информация о купоне', {
            'fields': ('coupon', 'success', 'error_message')
        }),
        ('Информация о пользователе', {
            'fields': ('user_phone', 'user_ip', 'user_agent')
        }),
        ('Финансовая информация', {
            'fields': ('order_id', 'order_total', 'discount_amount')
        }),
        ('Временная метка', {
            'fields': ('used_at',)
        }),
    )
    
    readonly_fields = ['used_at']
    
    def has_add_permission(self, request):
        # Запрещаем ручное создание логов
        return False
