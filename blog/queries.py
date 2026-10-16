from blog.models import Post
from django.db.models import Count


def get_front_page_posts():
    return Post.objects.select_related(
        'author', 'author__profile', 'category'
    ).prefetch_related('tags').annotate(
        comment_count=Count('comments', distinct=True)
    )
