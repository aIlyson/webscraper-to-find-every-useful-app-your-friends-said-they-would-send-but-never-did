Este é um webscraping feito para facilitar uma análise, sem precisar fazer isso manualmente. O objetivo era coletar os nomes de todos os concorrentes de aplicativos disponíveis na Play Store relacionados a um tema específico.

## Features
- raspagem automatizada dos nomes dos aplicativos da Play Store a partir de uma URL específica.
- carregamento dinâmico da página com múltiplos scrolls
- filtragem e listagem dos nomes únicos dos apps encontrados
- suporte para modo headless (navegador invisível) para maior velocidade e menor uso de recursos
- salva a lista de aplicativos em um arquivo `.txt` para análise

Basta executar o script, informar a URL da Play Store (ou usar a padrão), e aguardar o resultado. É necessário o ChromeDriver instalado.