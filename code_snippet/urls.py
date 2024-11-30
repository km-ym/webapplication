from django.contrib import admin
from django.urls import path
from snippet import views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.TopView.as_view(), name="top"),
    path("list/", views.CodeListView.as_view(), name="list"),
    path("category/<str:category>", views.CategoryView.as_view(), name="category"),
    path('tag/<str:tag>', views.TagView.as_view(), name='tag'),
    path("list/new", views.CodeCreateView.as_view(), name="new"),
    path("list/edit/<int:pk>", views.CodeUpdateView.as_view(), name="edit"),
    path("list/detail/<int:pk>", views.CodeDetailView.as_view(), name="detail"),
    path('account/', include('allauth.urls')),
    path('favorite/', views.FollowCodeView.as_view(), name='favorite'),
    path('code/<int:code_id>/favorite/', views.FollowCodeView.as_view(), name='favorite_detail'),
    ]