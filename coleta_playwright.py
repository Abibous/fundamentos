from playwright.sync_api import sync_playwright

# Inicializa o gerenciador de conexões do Playwright
with sync_playwright() as p:
    # 1. Lança o navegador Chromium no modo VISUAL (headless=False)
    # slow_mo=500 adiciona uma pausa de 500 milissegundos entre as ações para acompanharmos
    browser = p.chromium.launch(headless=False, slow_mo=500)

    # 2. Cria um novo contexto de navegação simulando uma resolução de tela específica
    contexto = browser.new_context(
        viewport={"width": 375, "height": 812}
    )

    # 3. Abre uma nova aba (Page) associada a este contexto isolado
    pagina = contexto.new_page()

    # 4. Navega até a URL correspondente
    pagina.goto("https://practicesoftwaretesting.com/")

    # Captura o título da página
    titulo = pagina.title()
    print(f"Título da página carregada: {titulo}")

    # Tira um print screen da tela para comprovação do teste
    pagina.screenshot(path="visualizacao_mobile.png")

    # 5. Sempre encerre o contexto e o navegador ao finalizar
    contexto.close()
    browser.close()