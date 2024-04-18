"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import QuestionListView, PostDetailView, QuestionCreateView, ChoiceCreateView, QuestionUpdateView, QuestionDeleteView
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:question_id>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/practice/", views.Practice.as_view(), name="practice"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('question/new/', QuestionCreateView.as_view(), name='question_new'),
    path('question/<int:pk>/choice/new/', ChoiceCreateView.as_view(), name='choice_new'),
    path('question/<int:pk>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('homepage/', views.HomePageView.as_view(), name='home'),
    
]