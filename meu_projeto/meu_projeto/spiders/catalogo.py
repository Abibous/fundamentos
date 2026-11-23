import scrapy
# Importamos o Item Loader do Scrapy e o nosso Item estruturado
from scrapy.loader import ItemLoader
from meu_projeto.items import LivroItem

class CatalogoLoaderSpider(scrapy.Spider):
    name = "catalogo"
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        livros = response.css("article.product_pod")

        for livro in livros:
            # 1. Instanciamos o Loader passando o Item desejado e o seletor correspondente
            loader = ItemLoader(item=LivroItem(), selector=livro)

            # 2. Adicionamos os caminhos CSS aos respectivos campos
            loader.add_css("titulo", "h3 a::attr(title)")
            loader.add_css("preco", "p.price_color::text")
            loader.add_css("disponibilidade", "p.instock.availability::text")

            # 3. Retornamos o item totalmente carregado e limpo
            yield loader.load_item()

        # 4. Busca o link da proxima pagina e, se existir, segue para ela
        proxima_pagina = response.css("li.next a::attr(href)").get()
        if proxima_pagina is not None:
            yield response.follow(proxima_pagina, callback=self.parse)
