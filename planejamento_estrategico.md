# Planejamento Estratégico de Coleta de Dados

Relatório da Aula 5.1 (Issue #10): análise técnica de 4 plataformas para escolher a ferramenta de coleta ideal (HTTPX, Scrapy ou Playwright), seguindo a árvore de decisão do web scraping.

## 1. SDGs / ONU Brasil
**URL:** https://brasil.un.org/pt-br/sdgs

### Testes de inspeção
- **Aba Network (Fetch/XHR):** a página faz uma chamada `POST` para `api.uninfo.org/v0.2/plan/public/search`, que retorna JSON. Porém, ao analisar a resposta (aba Preview), os dados são uma lista paginada de planos administrativos da ONU (ex.: "BOS"), e não o conteúdo dos 17 ODS. Ou seja, essa API alimenta apenas uma parte secundária da página.
- **JavaScript desativado:** o conteúdo principal (os ODS) continua aparecendo normalmente, o que mostra que ele já vem pronto no HTML estático. Com o JS desativado, nenhuma chamada aparece em Fetch/XHR, pois elas são feitas pelo próprio JavaScript.

### Biblioteca ideal
**HTTPX + BeautifulSoup**

### Justificativa técnica
O conteúdo desejado não vem de uma API JSON, mas está presente no HTML estático da página. Assim, não é necessário simular um navegador real (Playwright), e como a coleta é de uma única página, também não é preciso um framework de coleta em larga escala (Scrapy). HTTPX + BeautifulSoup é a solução mais simples, lógica e com maior performance.

### robots.txt
- O caminho `/pt-br/sdgs` **não está bloqueado**, então a coleta é permitida.
- Restrições existentes (que não afetam esta página): áreas administrativas e de usuário (`/admin/`, `/user/login`...), a busca interna (`/search/`) e URLs com filtros (`?f[0]=`), além de arquivos internos do Drupal (`/core/`, `/profiles/`).
- Não há `Crawl-delay` nem `Sitemap` definidos. Mesmo assim, por boa prática, o raspador deve usar um `User-Agent` realista e pausas entre requisições.


## 2. UNESCO Core Data Portal
**URL:** https://core.unesco.org/en/home?biennium=42&quarter=2024Q1

### Testes de inspeção
- **Aba Network (Fetch/XHR):** a página faz chamadas que retornam JSON, como `beneficiary` e `contributors` (listas com dados por país, ~180 itens) e `world.topo.json` (o desenho do mapa-múndi). A URL da API é `https://core.unesco.org/en/map-chart/beneficiary`.
- **JavaScript desativado:** apenas o mapa interativo (com as contribuições dos países para a UNESCO) desaparece. O restante do conteúdo continua aparecendo, ou seja, vem pronto no HTML estático. O mapa é montado pelo JavaScript a partir das APIs acima.

### Biblioteca ideal
**Scrapy**

### Justificativa técnica
O site possui uma API JSON (o que, pela árvore de decisão, indicaria o HTTPX), mas o robots.txt bloqueia o caminho dessa API (`/*/map-chart*`), então os dados do mapa não podem ser coletados. Já o restante do conteúdo está disponível diretamente no HTML. Como o site possui um sitemap (`sitemap.xml`) que lista suas páginas, é possível fazer uma coleta em larga escala, o que torna o Scrapy a escolha ideal: ele possui o `SitemapSpider` para ler o sitemap e, com a configuração `ROBOTSTXT_OBEY = True`, ignora automaticamente as páginas bloqueadas pelo robots.txt.

### robots.txt
- **`Disallow: /*/map-chart*`**: bloqueia a API do mapa, o que impediu a coleta direta via JSON.
- **`Disallow: /*/home*?*`**: bloqueia a página inicial com filtros, incluindo a URL do exercício (`/en/home?biennium=42&quarter=2024Q1`). A página `/en/home` sem filtros continua permitida.
- Outros bloqueios: páginas de busca e explore, exportações (`export`, `pdf`, `table-export`) e páginas de financiamento, projetos e países quando acessadas com filtros (`?`).
- **Sitemap:** `http://core.unesco.org/sitemap.xml`, uma lista oficial das páginas do site, útil para a coleta em larga escala.
- Não há `Crawl-delay`. Mesmo assim, o raspador deve usar um `User-Agent` realista e pausas entre requisições.


## 3. European Data Portal
**URL:** https://data.europa.eu/data/datasets?locale=pt

### Testes de inspeção
- **Aba Network (Fetch/XHR):** a página faz várias chamadas que retornam JSON, com informações de datasets, vocabulários e séries. Todas passam pelo mesmo endereço de API: `https://data.europa.eu/api/hub/search/search?...`. A chamada principal traz os datasets (título, descrição, país, formatos, licença, publicador), com paginação (`limit=10&page=0`) e ordenação (`sort=...`).
- **JavaScript desativado:** todo o conteúdo desaparece e fica apenas uma tela de carregamento. O site é uma SPA (Single Page Application): o HTML vem praticamente vazio e é o JavaScript que monta a página a partir da API.

### Biblioteca ideal
**HTTPX** (tecnicamente), porém **a coleta não é permitida pelo robots.txt**.

### Justificativa técnica
Como os dados vêm de uma API JSON, a ferramenta ideal pela árvore de decisão seria o HTTPX, consumindo o JSON diretamente. A API também já possui paginação (`page` e `limit`), o que permitiria uma coleta em larga escala apenas trocando o número da página. Porém, na prática, seguindo as diretrizes de polidez, nenhuma das formas de coleta aprendidas é permitida: a API está marcada como `Disallow` no robots.txt. O HTML estático não serve como alternativa (vem vazio), e usar o Playwright para renderizar a página faria o navegador acessar a mesma API não permitida. A alternativa correta seria verificar se o portal oferece uma API oficial documentada para desenvolvedores.

### robots.txt
- **`Disallow: /*search?*`**: não permite o acesso à API de busca inteira (`/api/hub/search/search?...`), que é de onde vêm todos os dados da página.
- **Filtros não permitidos:** `/*&sort=*` (ordenação, presente na própria chamada dos datasets), `/*&bounds=*`, `/*?query=*`, `/*?keywords=*` e `/*?title=*`.
- Também não permite as exportações de datasets em `.jsonld` e `.rdf`.
- As regras específicas para `Googlebot` e `Bingbot` valem apenas para esses robôs; um raspador próprio segue o bloco `User-agent: *`.
- O site possui 4 sitemaps (`/sitemap.xml`, `/en/sitemap.xml` e dois do `/dashboard/`), mas as páginas listadas também dependem de JavaScript para mostrar o conteúdo.
- Não há `Crawl-delay`.


## 4. FAO Brasil (Organização das Nações Unidas para a Alimentação e a Agricultura)
**URL:** https://www.fao.org/brasil/noticias/pt/

### Testes de inspeção
- **Aba Network (Fetch/XHR):** a primeira chamada encontrada (`nl-api.insight.sitefinity.com/collect/.../interactions`) é de um serviço de análise de visitantes (Sitefinity Insight): ela apenas envia dados sobre a navegação, sem retornar conteúdo (por isso o Preview fica vazio). A chamada que realmente traz as notícias é `https://www.fao.org/brasil/news/GetContent/1/pt/?_=...`, que não retorna JSON, e sim um trecho de HTML já com as notícias montadas. O número `1` na URL indica a página de notícias, e o parâmetro `?_=` é apenas um carimbo de tempo para evitar cache.
- **JavaScript desativado:** a estrutura do site continua aparecendo, mas as notícias (o conteúdo principal) não carregam. Isso confirma que elas são buscadas pelo JavaScript através da chamada `GetContent`.

### Biblioteca ideal
**Scrapy**

### Justificativa técnica
Os dados não vêm de uma API JSON, mas de uma chamada que retorna HTML pronto, que pode ser acessada diretamente, sem precisar simular um navegador (Playwright). Como as notícias são divididas em muitas páginas (`/GetContent/1/pt/`, `/2/pt/`, `/3/pt/`...), trata-se de uma coleta em larga escala, o que torna o Scrapy a escolha ideal: ele lê o HTML com seletores CSS, segue a paginação automaticamente e já possui recursos de polidez (respeitar o robots.txt, pausas entre requisições e novas tentativas em caso de erro).

### robots.txt
- Nem a página `/brasil/noticias/pt/` nem a chamada `/brasil/news/GetContent/...` estão bloqueadas, então a coleta é **permitida**. É o único dos 4 sites em que o caminho técnico ideal também é liberado.
- **`Disallow: /*?id=*`**: URLs com o parâmetro `?id=` não são permitidas; é preciso garantir que a paginação não use esse formato.
- Outros bloqueios: partes internas do sistema TYPO3 (`/index.php`, `/typo3/`, `/t3lib/`, `/*&type=98`) e pastas de arquivos enviados (`/fileadmin/user_upload/PermRep/` e `/en/`).
- O site lista 6 sitemaps, mas todos são de outras seções da FAO (newsroom, americas, europe, world-food-day...), nenhum específico de `/brasil/`.
- Não há `Crawl-delay`. Mesmo assim, o raspador deve usar um `User-Agent` realista e pausas entre requisições.

## Conclusão

| Site | API JSON? | Conteúdo no HTML? | Escala | Ferramenta | robots.txt |
|---|---|---|---|---|---|
| ONU Brasil | Só de dados secundários (planos "BOS") | Sim | Uma página | HTTPX + BeautifulSoup | Permitido |
| UNESCO | Sim (mapa), mas não permitida | Sim (exceto o mapa) | Larga (sitemap) | Scrapy | Permitido sem filtros; API do mapa não |
| European Data Portal | Sim, mas não permitida | Não (SPA) | Larga (paginação da API) | HTTPX (tecnicamente) | Coleta não permitida |
| FAO Brasil | Não (chamada retorna HTML) | Não na página principal, mas via `GetContent` | Larga (paginação) | Scrapy | Permitido |

A análise mostrou que a escolha da ferramenta não depende só da técnica: em dois dos quatro sites, o caminho mais eficiente (consumir a API diretamente) não é permitido pelo robots.txt. Por isso, além de seguir a árvore de decisão, é essencial verificar o robots.txt antes de qualquer coleta, e respeitar as diretrizes de polidez (User-Agent realista, pausas entre requisições e tratamento de erros).