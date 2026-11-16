# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class ValidacaoLivroPipeline:
    def process_item(self, item, spider):
        # 1. Verifica se o campo 'preco' existe e está populado
        preco = item.get("preco")
        if not preco:
            # Se não houver preço, descarta o item para que não seja exportado
            raise DropItem(f"Item descartado por falta de preço: {item}")

        # 2. Converte o valor string (ex: '51.77') para um float real do Python
        try:
            item["preco"] = float(preco)
        except ValueError:
            raise DropItem(f"Preço inválido para conversão numérica: {preco}")

        return item

import sqlite3

class SQLitePipeline:
    # Este método é executado de forma automática assim que a Spider inicializa
    def open_spider(self, spider):
        # Abre ou cria o arquivo do banco de dados na raiz do projeto
        self.conexao = sqlite3.connect("catalogo_livros.db")
        self.cursor = self.conexao.cursor()
        # Cria a tabela caso ela não exista no arquivo
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                preco REAL,
                disponibilidade TEXT
            )
        """)
        self.conexao.commit()

    # Este método é executado automaticamente quando a Spider encerra a coleta
    def close_spider(self, spider):
        self.conexao.close()

    # Este método processa cada um dos itens enviados pela Spider
    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO livros (titulo, preco, disponibilidade)
            VALUES (?, ?, ?)
        """, (
            item.get("titulo"),
            item.get("preco"),
            item.get("disponibilidade")
        ))
        self.conexao.commit()
        return item
