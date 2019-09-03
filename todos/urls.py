from django.urls import path
from . import views
from django.views.generic import TemplateView


# para utilizar na url 'todos:nome-da-url'
# app_name = 'todos'
urlpatterns = [
    path('agora/', views.tempo_atual, name='agora'),
    path('<int:pk>/', views.view, name='todos-view'),
    path('template-view/', TemplateView.as_view(template_name='todos/template-teste.html')),
    path('lista/', views.TodoListView.as_view()),
    path('<int:pk>/detail/', views.TodoDetail.as_view(), name='todos-detail'),
]
