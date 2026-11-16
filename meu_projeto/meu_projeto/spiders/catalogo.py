import scrapy

class CatalogoSpider(scrapy.Spider):
    name = "catalogo"
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        # Localiza e seleciona todos os blocos de livros da vitrine
        livros = response.css("article.product_pod")

        for livro in livros:
            # Extrai os dados internos usando seletores locais (indicados pelo ponto inicial ".")
            titulo = livro.css("h3 a::attr(title)").get()
            preco = livro.css("p.price_color::text").get()
            # Extrai o texto de disponibilidade em estoque (junta os pedacos de texto e remove espacos extras)
            disponibilidade = "".join(livro.css("p.instock.availability::text").getall()).strip()

            # Entrega os dados coletados estruturados
            yield {
                "titulo": titulo,
                "preco": preco,
                "disponibilidade": disponibilidade,
            }
        
         # 2. Busca o link da próxima página
        proxima_pagina = response.css("li.next a::attr(href)").get()

        # 3. Se o link existir, segue o link chamando este mesmo método parse
        if proxima_pagina is not None:
            yield response.follow(proxima_pagina, callback=self.parse)
