from django.db import models

class Brewery(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  # Usando o ID fornecido como chave primária
    name = models.CharField(max_length=255,blank=True, null=True )
    brewery_type = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True )
    state_province = models.CharField(max_length=100,blank=True, null=True )
    postal_code = models.CharField(max_length=20,blank=True, null=True )
    country = models.CharField(max_length=100,blank=True, null=True )
    longitude = models.FloatField()
    latitude = models.FloatField()
    phone = models.CharField(max_length=20,blank=True, null=True )
    website_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'staging_cervejarias'  # Definindo o nome da tabela como 'raw_cervejarias'


    def __str__(self):
        return self.name

class ModelContagemCervejaria(models.Model):
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    brewery_type = models.CharField(max_length=100)
    count = models.IntegerField()

    class Meta:
        db_table = 'model_contagem_cervejaria'

    def __str__(self):
        return f'{self.count} cervejarias - {self.brewery_type} em {self.city or self.state_province or self.country}'
