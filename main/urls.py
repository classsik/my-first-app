from django.urls import path
from django.contrib.auth import views
from .views import index, other_page, SPasswordChangeView, LogoutView, SLoginView, RegisterFormView, news_list, news_detail, lessons_shedule
from django.conf.urls import url
app_name = 'main'
urlpatterns =[
    path('news/', news_list, name='news'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('shedule/', lessons_shedule, name='shedule'),
    path('accounts/password/change/', SPasswordChangeView.as_view(), name='password_change'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/register/', RegisterFormView.as_view(), name='register'),
    path('accounts/login/', SLoginView.as_view(), name='login'),
    path('', index, name='index'),
]