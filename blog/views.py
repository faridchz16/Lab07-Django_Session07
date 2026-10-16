from django.shortcuts import render, get_object_or_404
from blog.queries import get_front_page_posts
from blog.models import Post


def front_page(request):
    posts = get_front_page_posts()
    return render(request, 'blog/front_page.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'author__profile', 'category').prefetch_related('tags', 'comments'),
        id=post_id
    )
    return render(request, 'blog/post_detail.html', {'post': post})
