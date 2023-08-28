from django.urls import path
from .views import detail

urlpatterns = [
    path('<int:category_pk>/<int:pk>/', detail, name='detail')
]
