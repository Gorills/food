from .forms import CouponApplyForm

def coupon_form(request):
    return {'coupon_form': CouponApplyForm()}


