from .models import Subdomain
from .utilites import get_protocol, get_subdomain, get_domain

def subdomain(request):
    return {'subdomain': get_subdomain(request)}

def domain(request):
    return {'domain': get_domain(request)}

def subdomains(request):
    return {'subdomains': Subdomain.objects.all().order_by('name')}


def protocol(request):
    return {'protocol': get_protocol(request)}


def get_site(request):
    
    return {'site': f'{get_protocol(request)}://' + str(request.META['HTTP_HOST'])}





