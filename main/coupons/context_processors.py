from coupons.models import Coupon
from .forms import CouponApplyForm

def coupon_form(request):
    return {'coupon_form': CouponApplyForm()}


def coupon(request):
    
    coupon_count = Coupon.objects.all().count()

    return {'coupon_count': coupon_count}
    

