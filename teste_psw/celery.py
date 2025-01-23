# teste_psw/celery.py
import logging
import os
from celery import Celery
from celery.signals import task_postrun, task_failure

# Define o módulo de configuração do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teste_psw.settings')

# Cria uma instância do Celery
app = Celery('teste_psw')

# Usando o broker Redis
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega tarefas de todos os aplicativos Django registrados
app.autodiscover_tasks()

# Configuração de Logging
logger = logging.getLogger('celery')

# Capturar eventos de execução das tarefas Celery

@task_postrun.connect
def task_done(sender=None, task_id=None, **kwargs):
    logger.info(f"Tarefa {task_id} foi finalizada com sucesso.")

@task_failure.connect
def task_failed(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(f"Tarefa {task_id} falhou com exceção: {exception}")