from django.urls import path
from .views import AppView, SectionView


app_name = 'app'
urlpatterns = [
    path('', AppView.as_view()),
    path('section/', SectionView.as_view()),
]
