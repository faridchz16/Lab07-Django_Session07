from blog.models import Post, Author, Category, Tag, Comment
from django.db.models import Count

QUESTIONS = {
    "q1": {
        "description": "All posts ordered by creation date descending",
        "func": lambda: Post.objects.all().order_by('-created_at')
    },
    "q2": {
        "description": "Posts written by authors whose name starts with 'A'",
        "func": lambda: Post.objects.filter(author__name__startswith='A')
    },
    "q3": {
        "description": "Posts belonging to the 'Tecnología' category",
        "func": lambda: Post.objects.filter(category__name='Tecnología')
    },
    "q4": {
        "description": "Posts tagged with 'django'",
        "func": lambda: Post.objects.filter(tags__name='django')
    },
    "q5": {
        "description": "Posts annotated with comment count (n_comments) and tag count (n_tags)",
        "func": lambda: Post.objects.annotate(n_comments=Count('comments', distinct=True), n_tags=Count('tags', distinct=True))
    },
    "q6": {
        "description": "Authors who have written at least 3 posts",
        "func": lambda: Author.objects.annotate(post_count=Count('posts')).filter(post_count__gte=3)
    },
    "q7": {
        "description": "Posts ordered by author name ascending and title descending",
        "func": lambda: Post.objects.all().order_by('author__name', '-title')
    },
    "q8": {
        "description": "Categories that have at least 2 posts",
        "func": lambda: Category.objects.annotate(post_count=Count('posts')).filter(post_count__gte=2)
    },
}
