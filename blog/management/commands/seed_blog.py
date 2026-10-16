from django.core.management.base import BaseCommand
from django.db import connection
from blog.models import Author, Profile, Category, Tag, Post, Comment
from blog.seed_data import AUTHORS, CATEGORIES, TAGS, POSTS, COMMENTS


class Command(BaseCommand):
    help = 'Seeds the database with fixed blog data (4 authors, 15 posts with images, 23 comments) and resets IDs to start at 1'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing blog data and resetting primary keys...')
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Profile.objects.all().delete()
        Author.objects.all().delete()

        # Reset SQLite auto-increment sequences so IDs start fresh at 1
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('blog_author', 'blog_profile', 'blog_category', 'blog_tag', 'blog_post', 'blog_comment');")

        self.stdout.write('Creating categories...')
        category_objects = {}
        for cat_name in CATEGORIES:
            category_objects[cat_name] = Category.objects.create(name=cat_name)

        self.stdout.write('Creating tags...')
        tag_objects = {}
        for tag_name in TAGS:
            tag_objects[tag_name] = Tag.objects.create(name=tag_name)

        self.stdout.write('Creating authors and profiles...')
        author_objects = {}
        for author_data in AUTHORS:
            author = Author.objects.create(
                name=author_data["name"],
                email=author_data["email"]
            )
            Profile.objects.create(
                author=author,
                bio=author_data["bio"],
                website=author_data["website"]
            )
            author_objects[author_data["email"]] = author

        self.stdout.write('Creating posts with respective images...')
        post_objects = {}
        for post_data in POSTS:
            author = author_objects[post_data["author_email"]]
            category = category_objects.get(post_data["category"])
            post = Post.objects.create(
                title=post_data["title"],
                content=post_data["content"],
                author=author,
                category=category,
                image_url=post_data.get("image_url")
            )
            for tag_name in post_data["tags"]:
                if tag_name in tag_objects:
                    post.tags.add(tag_objects[tag_name])
            post_objects[post_data["title"]] = post

        self.stdout.write('Creating comments...')
        for comment_data in COMMENTS:
            post = post_objects[comment_data["post_title"]]
            Comment.objects.create(
                post=post,
                author_name=comment_data["author_name"],
                content=comment_data["content"]
            )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded blog! Authors: {Author.objects.count()}, '
            f'Posts: {Post.objects.count()}, Comments: {Comment.objects.count()} (IDs reset to 1-15)'
        ))
