from django.urls import path
from . import views
from data.views import description, scrap

urlpatterns = [
    path('scrap',scrap.as_view()),
    path('description',description.as_view()),

]