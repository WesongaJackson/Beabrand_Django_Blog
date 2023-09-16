
from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView,CommentCreateView,PostDeleteView,CommentDeleteView

urlpatterns = [
    path('',PostListView.as_view(),name='blog-home' ),
    path('post/<int:pk>/comment/',CommentCreateView.as_view(),name='add-comment' ),

    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail' ),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete' ),
    path('comment/<int:pk>/delete/',CommentDeleteView.as_view(),name='comment-delete' ),

    path('post/new/',PostCreateView.as_view(),name='post-create' ),
    path('about',views.about,name='blog-about' ),
]
