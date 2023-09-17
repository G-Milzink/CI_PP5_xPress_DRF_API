from django.urls import path
from collages import views

urlpatterns = [
    path('collages/', views.CollageList.as_view()),
]
