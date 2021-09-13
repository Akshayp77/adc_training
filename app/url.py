from django.contrib import admin
from django.urls import path,include
from . import views
from .views import recommended_articles, user_auth_api,login,liked_article


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',user_auth_api.as_view()),
    path('login',login.as_view()),
    path('liked',liked_article.as_view()),
    path('recommended',recommended_articles.as_view())

]