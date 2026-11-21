import httpx

url = "https://api.practicesoftwaretesting.com/products"

# Cabeçalho simulado: faz a requisição parecer vir de um navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# Parâmetro de filtragem: só produtos da categoria Power Tools
params = {
    "by_category_slug": "power-tools"
}

resposta = httpx.get(url, headers=headers, params=params)

if resposta.status_code == 200:
    produtos = resposta.json().get("data", [])

    # Ordena do mais barato para o mais caro
    produtos = sorted(produtos, key=lambda p: p.get("price", 0))

    print(f"{len(produtos)} produtos encontrados em Power Tools:\n")
    for produto in produtos:
        nome = produto.get("name")
        preco = produto.get("price")
        print(f"{nome:<25} $ {preco:.2f}")
else:
    print(f"Erro na requisição: {resposta.status_code}")