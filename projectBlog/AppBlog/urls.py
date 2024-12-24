from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name= 'index'),
    path('register', views.RegisterView.as_view(), name= 'register'),
    path('home',views.HomeView.as_view(), name= 'home'),
    path('create',views.CreatePost.as_view(), name='createpost'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/<int:id>', views.postRead, name='posts'),
    path('ownpost',views.PostCreatedbyUsser.as_view(), name='ownpost'),
    path('posts/edit/<int:id>', views.postEdit, name='edit'),
    path('posts/delete/<int:id>', views.postDelete, name='delete'),
]