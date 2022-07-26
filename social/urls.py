from django.urls import path
from . import views

# social:top などの名前指定に必要な表記
app_name = 'social'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('<int:genre_id>', views.Top.as_view(), name='top'),
    path('thread/<int:thread_id>', views.ViewPosts.as_view(), name="view_posts"),
    path('create/', views.CreateThread.as_view(), name="create_thread"),
]
