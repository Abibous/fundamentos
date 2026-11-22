import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    contexto = browser.new_context()
    pagina = contexto.new_page()

    # 1. Navega até o site de teste
    pagina.goto("https://practicesoftwaretesting.com/")

    # 2. Aguarda até que a rede pare de fazer requisições de inicialização
    pagina.wait_for_load_state("networkidle")

    # 3. Executa um loop de rolagem para carregar mais produtos na vitrine
    print("Iniciando rolagens para carregar novos produtos...")
    for _ in range(4):
        # Rola a tela para baixo
        pagina.evaluate("window.scrollBy(0, 1000)")
        # Aguarda um pequeno intervalo de carregamento dinâmico
        time.sleep(1.5)

    # 4. Aguarda explicitamente até que o rodapé ou um seletor específico confirme o carregamento
    pagina.wait_for_selector("a.card")

    # 5. Coleta os produtos finais carregados na vitrine expandida
    produtos = pagina.locator("a.card").all()
    print(f"Total de produtos visíveis na tela após rolagens: {len(produtos)}")

    contexto.close()
    browser.close()