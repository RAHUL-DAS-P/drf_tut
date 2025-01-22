from django.urls import path
from .views import loading

urlpatterns = [
    path('', loading),
]