from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views  # funcoes

# urlpatterns = [
#     path('root/', views.api_root),
#     path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
#     path('users/', views.UserList.as_view(), name='user-list'),
#     path('users/<int:pk>/', views.UserDetail.as_view()),
#     path('users/<int:pk>/hightlight/', views.SnippetHighlight.as_view()),
#     #path('snippets/<int:pk>/', views.snippet_detail),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(),
         name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(),
         name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(),
         name='snippet-highlight'),
    path('users/', views.UserViewSet.as_view(),
         name='users-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(),
         name='user-detail')
])
