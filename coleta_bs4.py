import httpx
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 1. Baixa o código HTML plano da página alvo
resposta = httpx.get(url, headers=headers)

if resposta.status_code == 200:
    # 2. Transmite o texto do HTML para análise do BeautifulSoup
    soup = BeautifulSoup(resposta.text, "html.parser")

    # 3. Localiza os invólucros que contêm cada um dos livros da vitrine
    livros = soup.find_all("article", class_="product_pod")

    for livro in livros:
        # Encontra o cabeçalho 'h3' e o elemento 'a' interno
        link_livro = livro.find("h3").find("a")

        # Extrai o valor contido no atributo 'title' do link
        titulo = link_livro["title"]

        # Encontra o parágrafo de preço e extrai o texto da classe 'price_color'
        preco = livro.find("p", class_="price_color").text

        # Imprime os resultados de forma organizada
        print(f"Título: {titulo} | Preço: {preco}")
else:
    print(f"Erro ao acessar a página: {resposta.status_code}")