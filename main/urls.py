from django.urls import path
from django.contrib.auth import views
from .views import index, other_page, SPasswordChangeView, LogoutView, SLoginView, RegisterFormView, news_list, news_detail, lessons_shedule, call_shedule, like_news
from django.conf.urls import url
from . import views
app_name = 'main'
urlpatterns =[
    path('news/', news_list, name='news'),
    path('like/', like_news, name='like_news'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('calls/', call_shedule, name='call'),
    path('shedule/', lessons_shedule, name='shedule'),
    path('course/module/order/', views.ModuleOrderView.as_view(),name='module_order'),
    path('course/content/order/', views.ContentOrderView.as_view(), name='content_order'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/subject/<slug:subject>)/', views.CourseListView.as_view(), name='course_list_subject'),
    path('courses/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
    path('course/content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('course/module/<int:module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('course/module/<int:module_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('course/<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('course/mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('accounts/password/change/', SPasswordChangeView.as_view(), name='password_change'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/register/', RegisterFormView.as_view(), name='register'),
    path('accounts/login/', SLoginView.as_view(), name='login'),
    path('', index, name='index'),
]
