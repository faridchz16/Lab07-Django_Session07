from blog.models import Post, Author, Category, Tag
from django.db.models import Count


def q1():
    return Post.objects.all().order_by('-created_at')


def q2():
    return Post.objects.filter(author__name__startswith='A')


def q3():
    return Post.objects.filter(category__name='Tecnología')


def q4():
    return Post.objects.filter(tags__name='django')


def q5():
    return Post.objects.annotate(
        n_comments=Count('comments', distinct=True),
        n_tags=Count('tags', distinct=True)
    )


def q6():
    return Author.objects.annotate(post_count=Count('posts')).filter(post_count__gte=3)


def q7():
    return Post.objects.all().order_by('author__name', '-title')


def q8():
    return Category.objects.annotate(post_count=Count('posts')).filter(post_count__gte=2)
