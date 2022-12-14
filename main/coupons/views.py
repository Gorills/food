from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    
    coupon = request.POST['coupon']
    
    try:
        coupon = Coupon.objects.get(code=coupon,
                                    valid_from__lte=now,
                                    valid_to__gte=now,
                                    active=True)
        request.session['coupon_id'] = coupon.id
        
    except:
        request.session['coupon_id'] = None            
    return redirect('home')