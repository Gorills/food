from django.shortcuts import render, get_object_or_404
from .models import Post, BlogCategory, BlogSetup



from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except Exception:
    theme_address = 'fast_theme'


# Create your views here.

def blog(request):
    last = Post.objects.filter(published=True).exclude(image=None).exclude(parent=None).last()
    post = Post.objects.filter(published=True).order_by('-id')[1:2].first()
    posts_trio = Post.objects.filter(published=True).order_by('-id')[2:5]
    posts_all = Post.objects.filter(published=True).order_by('-id')[5:]
    max_post = Post.objects.filter(published=True)
    blog_settings = BlogSetup.objects.get()
    context = {
        'last': last,
        'post': post,
        'posts_trio': posts_trio,
        'posts_all': posts_all,
        'max_post': max_post,
        'blog_categorys': BlogCategory.objects.all(),
        'blog_settings': blog_settings,
    }
    

    return render(request, 'blog/blog.html', context)



def blog_category_detail(request, slug):
    blog_category = get_object_or_404(BlogCategory, slug=slug)

    last = Post.objects.filter(published=True, parent_id=blog_category.id).exclude(image=None).exclude(parent=None).last()
    post = Post.objects.filter(published=True, parent_id=blog_category.id).order_by('-id')[1:2].first()
    posts_trio = Post.objects.filter(published=True, parent_id=blog_category.id).order_by('-id')[2:5]
    posts_all = Post.objects.filter(published=True, parent_id=blog_category.id).order_by('-id')[5:]
    max_post = Post.objects.filter(published=True, parent_id=blog_category.id)
    context = {
        'blog_category': blog_category,
        'last': last,
        'post': post,
        'posts_trio': posts_trio,
        'posts_all': posts_all,
        'max_post': max_post,
        'blog_categorys': BlogCategory.objects.all(),
    }

    return render(request, 'blog/blog_catgory_detail.html', context)

def post_detail(request, slug, parent):
    
    context = {
        'post': get_object_or_404(Post, slug=slug)
    }

    return render(request, 'blog/post_detail.html', context)
