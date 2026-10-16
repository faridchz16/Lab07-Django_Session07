from django.urls import path
from blog.views import front_page, post_detail

urlpatterns = [
    path('', front_page, name='front_page'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]
