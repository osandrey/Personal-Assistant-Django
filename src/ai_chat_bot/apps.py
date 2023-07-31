from django.apps import AppConfig
from .views import run_polling
from multiprocessing import Process


class AiChatBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_chat_bot'

    def ready(self):
        bot_process = Process(target=run_polling)
        bot_process.start()
        print(f'Process started with name: {bot_process.name}')



