

from django.urls import path, re_path
from . import views
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Definir o esquema do Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API de Cervejarias",
      default_version='v1',
      description="Documentação da API para gerenciamento de cervejarias",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contato@cervejarias.com"),
      license=openapi.License(name="Licença MIT"),
   ),
   public=True,
)

urlpatterns = [
    path('breweries/', views.BreweryList.as_view(), name='brewery-list'),
    path('model-contagem/', views.ModelContagemCervejariaList.as_view(), name='model-contagem-list'),
    # URL para acessar a documentação Swagger
    re_path(r'^swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    # Você também pode gerar a documentação em formato JSON
    re_path(r'^swagger.json/', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
]