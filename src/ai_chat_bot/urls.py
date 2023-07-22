
from .views import main, redirect_check
from django.urls import path



app_name = 'ai_chat_bot'

urlpatterns = [
    path('', main, name='main'),
    path('/tg', redirect_check, name='redirect_check')
    ]