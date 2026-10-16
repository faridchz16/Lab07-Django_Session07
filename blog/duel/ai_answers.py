from blog.models import Post, Author, Category, Tag
from django.db.models import Count


def q1():
    # Correct
    return Post.objects.all().order_by('-created_at')


def q2():
    # Correct
    return Post.objects.filter(author__name__startswith='A')


def q3():
    # Correct but expensive or using icontains instead of exact
    return Post.objects.filter(category__name__icontains='Tecnología')


def q4():
    # Bug: missing distinct or filtering incorrectly
    return Post.objects.filter(tags__name__icontains='django')


def q5():
    # Bug: missing distinct causing multiplied counts
    return Post.objects.annotate(
        n_comments=Count('comments'),
        n_tags=Count('tags')
    )


def q6():
    # Correct
    return Author.objects.annotate(post_count=Count('posts')).filter(post_count__gte=3)


def q7():
    # Correct
    return Post.objects.all().order_by('author__name', '-title')


def q8():
    # Bug: incorrect filter condition
    return Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=2)
