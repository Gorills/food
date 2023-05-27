from django.shortcuts import redirect
from subdomains.models import Subdomain
from django.urls import reverse
from subdomains.utilites import get_subdomain

class SubdomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        subdomains = Subdomain.objects.all()

        if subdomains.exists() and not get_subdomain(request) and not self.is_home_page(request) and not request.path.startswith('/yafeed.xml') and not request.path.startswith('/sitemap.xml') and not request.path.startswith('/robots.txt') and not request.path.startswith('/admin/') and not request.path.startswith('/core/') and not request.path.startswith('/media/') and not request.path.startswith('/accounts/'):
            # Проверка наличия субдомена и отсутствия запроса к главной странице или административной странице
            return redirect('/') 

        response = self.get_response(request)
        return response

    @staticmethod
    def is_home_page(request):
        return request.path == reverse('home')

    @staticmethod
    def is_admin_page(request):
        return request.path.startswith(reverse('admin')) and len(request.path) == len(reverse('admin'))
