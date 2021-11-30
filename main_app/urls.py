from django.forms.models import fields_for_model
from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('posts/index/', views.posts_index, name='index'),
    path('posts/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
    path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
    path('posts/<int:post_id>/add_category/', views.add_category, name='add_category'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('like/<int:post_id>/', views.LikeView, name='like_post')
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)