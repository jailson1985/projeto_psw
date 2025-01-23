from datetime import datetime
import json
import os
from celery import shared_task
from django.db import IntegrityError 
from django.db.models import Count
import requests
from .models import Brewery, ModelContagemCervejaria
import logging

logger = logging.getLogger('celery')

@shared_task
def import_breweries_task():
    # URL base da API
    url = 'https://api.openbrewerydb.org/breweries'

    try:
        # Lista para armazenar todos os dados das cervejarias
        all_breweries = []

        # Parâmetros de página e limite de registros por página
        page = 1
        per_page = 50  # Número de resultados por página

        while True:
            # Parâmetros para a requisição
            params = {
                'page': page,
                'per_page': per_page
            }

            # Fazer a requisição para obter os dados da API
            response = requests.get(url, params=params)

            # Verificar se a resposta foi bem-sucedida
            if response.status_code == 200:
                data = response.json()

                # Se não houver dados, sai do loop
                if not data:
                    break

                # Adicionar os dados da página atual à lista de todas as cervejarias
                all_breweries.extend(data)

                # Incrementar o número da página
                page += 1
            else:
                return f"Erro ao acessar a API: {response.status_code}"

        # Criar um nome único para o arquivo, usando a data e hora atual
        file_name = f'raw_brewery_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        file_path = f'/app/case/file/{file_name}'  # Caminho para salvar no diretório local

        # Verificar se o diretório existe, caso contrário, criar
        if not os.path.exists('/app/case/file'):
            os.makedirs('/app/case/file')
        
        # Salvar o JSON no diretório local
        with open(file_path, 'w') as json_file:
            json.dump(all_breweries, json_file, indent=4)

        return f"Arquivo JSON salvo como {file_name} com {len(all_breweries)} cervejarias!"

    except requests.exceptions.RequestException as e:
        return f"Erro ao fazer a requisição para a API: {e}"
    except Exception as e:
        return f"Erro inesperado: {e}"

@shared_task
def import_breweries_from_file():
    # Caminho do diretório onde os arquivos JSON estão localizados
    directory_path = '/app/case/file'

    try:
        # Listar todos os arquivos do diretório
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        # Verificar se há arquivos no diretório
        if not files:
            return f"Erro: Nenhum arquivo encontrado no diretório {directory_path}."

        # Encontrar o arquivo com a maior data de modificação (mais recente)
        most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))

        # Caminho completo do arquivo mais recente
        file_path = os.path.join(directory_path, most_recent_file)

        # Abrir e ler o conteúdo do arquivo JSON
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        Brewery.objects.all().delete()

        # Processar e salvar os dados no banco de dados
        for brewery_data in data:
            # Garantir que os campos essenciais estão presentes
            if not brewery_data.get('name') or not brewery_data.get('city') or not brewery_data.get('country'):
                continue  # Ignora esta cervejaria se os campos essenciais estiverem ausentes

            # Verificar se latitude e longitude são válidos, e atribuir valores padrão se necessário
            latitude = brewery_data.get('latitude')
            longitude = brewery_data.get('longitude')

            # Tentar converter latitude e longitude para float, se não for possível, atribui 0.0
            try:
                latitude = float(latitude) if latitude is not None else 0.0
                longitude = float(longitude) if longitude is not None else 0.0
            except ValueError:
                latitude, longitude = 0.0, 0.0  # Caso a conversão falhe, atribui valores padrão

            # Criar ou atualizar o objeto Brewery
            Brewery.objects.update_or_create(
                id=brewery_data.get('id'),
                defaults={
                    'name': brewery_data.get('name'),
                    'brewery_type': brewery_data.get('brewery_type'),
                    'address_1': brewery_data.get('address_1'),
                    'address_2': brewery_data.get('address_2', ''),
                    'address_3': brewery_data.get('address_3', ''),
                    'city': brewery_data.get('city'),
                    'state_province': brewery_data.get('state_province', ''),
                    'postal_code': brewery_data.get('postal_code'),
                    'country': brewery_data.get('country'),
                    'longitude': longitude,
                    'latitude': latitude,
                    'phone': brewery_data.get('phone', ''),
                    'website_url': brewery_data.get('website_url', '')
                }
            )

        return f"Importação de cervejarias concluída a partir do arquivo {file_path}!"

    except FileNotFoundError:
        return f"Erro: O arquivo {file_path} não foi encontrado."
    except json.JSONDecodeError:
        return "Erro: O arquivo JSON está mal formatado."
    except IntegrityError as e:
        return f"Erro de integridade ao salvar os dados no banco de dados: {e}"
    except Exception as e:
        return f"Erro inesperado: {e}"
    
@shared_task
def count_brewery():
    # Agrupando as cervejarias por país, estado, cidade e tipo
    agrupamento = Brewery.objects.values('country', 'state_province', 'city', 'brewery_type').annotate(count=Count('id'))

    # Salvando ou atualizando os resultados na tabela de contagem
    for item in agrupamento:
        # Verifica se já existe uma entrada para esse agrupamento
        obj, created = ModelContagemCervejaria.objects.update_or_create(
            country=item['country'],
            state_province=item['state_province'],
            city=item['city'],
            brewery_type=item['brewery_type'],
            defaults={'count': item['count']},
        )

        if created:
            print(f'Nova contagem adicionada: {obj}')
        else:
            print(f'Contagem atualizada: {obj}')

    return "Contagem de cervejarias concluída"