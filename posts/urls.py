from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:id>/update/', views.update, name="update"),
    path('<int:id>/delete/', views.delete, name="delete"),

    path('hashtags/<int:id>/', views.hashtags, name="hashtags"),
    path('<int:id>/like/', views.like, name="like"),
    path('<int:id>/comment/create/', views.comment_create, name="comment_create"),
    path('<int:p_id>/comment/<int:c_id>/delete/',
         views.comment_delete, name="comment_delete"),
]
