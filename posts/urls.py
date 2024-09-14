from . import views
from django.urls import path

urlpatterns = [
    path("homepage/", views.homepage, name="post_home"),
    # path("", views.all_posts, name="all_posts"),
    path("", views.PostListCreateView.as_view(), name="list_posts"),
    path("<int:pk>/", views.PostRetrieveUpdateDeleteView.as_view(), name="post_detail"),
    # path("posts_for/<username>",views.ListPostsForAuthor.as_view(),name="posts_for_current_user",),
    path(
        "posts_for/",
        views.ListPostsForAuthor.as_view(),
        name="posts_for_current_user",
    ),
    # path(
    #     "<int:post_id>/",
    #     views.PostRetrieveUpdateDeleteView.as_view(),
    #     name="post_detail",
    # ),
    # path("<int:post_id>", views.get_post, name="post_detail"),
    # path("update/<int:post_id>", views.update_post, name="update_post"),
    # path("delete/<int:post_id>", views.delete_post, name="delete_post"),
]
