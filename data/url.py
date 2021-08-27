from django.contrib import admin
from django.urls import path
from . import views
from data.views import discription, scrap

urlpatterns = [
    path('scrap',scrap.as_view()),
    path('discription',discription.as_view()),

]