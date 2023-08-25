from django.urls import path
from .views import by_categories

urlpatterns = [
    path('<int:pk>/', by_categories, name='by_categories'),
]
