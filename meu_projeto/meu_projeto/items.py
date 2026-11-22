# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy
from itemloaders.processors import TakeFirst, MapCompose

# Função simples para limpar espaços e remover o símbolo de libra "£" do preço
def limpar_preco(valor):
    return valor.replace("£", "").strip()

class LivroItem(scrapy.Item):
    # TakeFirst() garante que o retorno será uma string única, e não uma lista ['livro']
    titulo = scrapy.Field(output_processor=TakeFirst())

    # MapCompose aplica funções de limpeza na entrada antes de retornar o resultado
    preco = scrapy.Field(
        input_processor=MapCompose(limpar_preco),
        output_processor=TakeFirst()
    )

    disponibilidade = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )




