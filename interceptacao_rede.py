from playwright.sync_api import sync_playwright

def processar_resposta_api(response):
    # 1. Filtramos apenas as respostas vindas do endpoint de produtos da API
    if "api.practicesoftwaretesting.com/products" in response.url:
        # Garantimos que a requisição foi bem sucedida (status 200)
        if response.status == 200:
            print(f"\n[API Interceptada] URL: {response.url}")

            # 2. Desempacotamos o JSON retornado
            dados = response.json()
            produtos = dados.get("data", [])

            print(f"--- Produtos extraídos diretamente do tráfego de rede ({len(produtos)}): ---")
            for produto in produtos:
                nome = produto.get("name")
                preco = produto.get("price")
                print(f"Nome: {nome} | Preço: ${preco}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    contexto = browser.new_context()
    pagina = contexto.new_page()

    # 3. Registramos o evento de escuta na página ANTES de navegar
    pagina.on("response", processar_resposta_api)

    # 4. Navegamos até a página de testes
    pagina.goto("https://practicesoftwaretesting.com/")

    # 5. Realizamos uma ação de clique na interface que força o disparo da API em segundo plano
    pagina.get_by_text("ForgeFlex Tools").click()

    # Aguardamos a rede ociosa para garantir que o processamento ocorreu
    pagina.wait_for_load_state("networkidle")

    contexto.close()
    browser.close()