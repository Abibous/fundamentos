from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    contexto = browser.new_context()
    pagina = contexto.new_page()

    # Navega até o e-commerce de testes
    pagina.goto("https://practicesoftwaretesting.com/")

    # 1. Localiza a barra de pesquisa e preenche com a busca
    pagina.get_by_placeholder("Search").fill("Pliers")

    # 2. Clica no botão de enviar busca (botão com ícone/texto de pesquisa)
    pagina.get_by_role("button", name="Search").click()

    # 3. Localiza e marca a caixa de seleção para filtrar apenas uma categoria
    pagina.locator("#filters").get_by_text("Hand Tools").click()

    # 4. Varre os novos produtos exibidos na tela após o filtro dinâmico rodar
    produtos = pagina.locator("a.card").all()

    print(f"--- Produtos encontrados ({len(produtos)}): ---")
    for produto in produtos:
        nome_produto = produto.locator("h5[data-test='product-name']").text_content()
        print(f"- {nome_produto.strip()}")

    contexto.close()
    browser.close()