import hashlib
import json
from blog.models import Post, Author, Comment
from django.db.models import Count


def action_posts_per_author(args):
    data = Author.objects.annotate(post_count=Count('posts')).values('name', 'post_count')
    return {"status": "ok", "data": list(data)}


def action_comments_of_post(args):
    post_id = args.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return {"status": "error", "message": f"Post {post_id} not found"}
    
    comments = post.comments.values('id', 'author_name', 'content', 'created_at')
    return {"status": "ok", "post_title": post.title, "comments": list(comments)}


def action_delete_comments_of_post(args):
    post_id = args.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return {"status": "error", "message": f"Post {post_id} not found"}
    
    count = post.comments.count()
    post.comments.all().delete()
    return {"status": "ok", "message": f"Deleted {count} comments for post {post_id}"}


REGISTRY = {
    "posts_per_author": {
        "func": action_posts_per_author,
        "destructive": False
    },
    "comments_of_post": {
        "func": action_comments_of_post,
        "destructive": False
    },
    "delete_comments_of_post": {
        "func": action_delete_comments_of_post,
        "destructive": True
    },
}


def compute_plan_hash(action, args):
    payload = json.dumps({"action": action, "args": args}, sort_keys=True)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12]


def execute_intent(intent_dict, approved=False, plan_hash=None):
    action = intent_dict.get("action")
    args = intent_dict.get("args", {})

    if action not in REGISTRY:
        return {"status": "denied", "reason": f"Action '{action}' is not allowed or does not exist in registry."}

    action_meta = REGISTRY[action]

    if action_meta["destructive"]:
        current_hash = compute_plan_hash(action, args)
        if not approved:
            return {
                "status": "approval_required",
                "action": action,
                "args": args,
                "plan_hash": current_hash,
                "message": f"Action '{action}' is destructive and requires approval. Run command again with --approve and --hash {current_hash}"
            }
        if plan_hash != current_hash:
            return {
                "status": "denied",
                "reason": "Plan hash mismatch or stale plan (data or parameters changed)."
            }

    # Execute safe or approved action
    try:
        result = action_meta["func"](args)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
