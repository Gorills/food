from .models import Subdomain



def get_protocol(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'

    return protocol


def get_hostname(request):
    return request.get_host()


def get_domain(request):

    hostname = get_hostname(request)
    domain_list = hostname.split('.')[1:]

    domain = '.'.join(domain_list)

    return domain

def get_subdomain(request):
    hostname = get_hostname(request)
    subdomain_parts = hostname.split('.')
    
    # Проверяем количество частей субдомена.
    # Если их меньше или равно 3, то это не субдомен четвертого уровня
    if len(subdomain_parts) <= 2:
        subdomain = subdomain_parts[0]
        return Subdomain.objects.filter(subdomain=subdomain).first()
    
    # Если количество частей субдомена больше 3, то игнорируем его
    return None


