from __future__ import absolute_import, unicode_literals

# Faço o import do Celery para garantir que o Celery seja executado quando o Django for iniciado.
from .celery import app as celery_app

__all__ = ('celery_app',)