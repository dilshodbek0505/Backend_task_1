from django.urls import path

from .views import (
    Task2View,
    Task3View,
    Task4View,
    Task5View,
    Task6View,
    Task8View
)


urlpatterns = [
    path('task-2/', Task2View.as_view()),
    path('task-3/', Task3View.as_view()),
    path('task-4/', Task4View.as_view()),
    path('task-5/', Task5View.as_view()),
    path('task-6/', Task6View.as_view()),
    path('task-8/', Task8View.as_view()),
]