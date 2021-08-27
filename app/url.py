from django.contrib import admin
from django.urls import path,include
from . import views
from .views import Recommended_articles, user_auth_api,login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',user_auth_api.as_view()),
    path('login',login.as_view()),
    path('recommended',Recommended_articles.as_view())

]