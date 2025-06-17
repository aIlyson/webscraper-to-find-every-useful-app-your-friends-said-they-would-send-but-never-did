from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import os
import sys
import platform
import re
from urllib.parse import urlparse

def get_default_paths():
    if platform.system() == 'Windows':
        # diretorios para a localização do seu chromedriver
        return [
            r'C:\Windows\chromedriver.exe',
            # ex: r'C:\Users\User\Downloads\chromedriver.exe'
        ]
    else:
        # ajuste estes caminhos, caso seja Linux/MacOS
        return [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver',
        ]

def get_chromedriver_path():
    """try to find chromedriver in common locations"""
    possible_paths = get_default_paths()

    for path in possible_paths:
        if os.path.exists(path):
            return path
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            return expanded_path
    
    print("\nErro: ChromeDriver não encontrado!")
    print("1. Acesse https://chromedriver.chromium.org/downloads")
    print("2. Baixe a versão correspondente ao seu navegador Chrome")
    print(f"3. Coloque em um dos diretórios: {possible_paths}")
    sys.exit(1)

def setup_driver():
    """configure Chrome options and create driver instance"""
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # modo headless - comente se quiser ver o navegador
    chrome_options.add_argument("--headless=new")
    
    try:
        driver_path = get_chromedriver_path()
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"\nerro ao iniciar o ChromeDriver: {str(e)}")
        sys.exit(1)

def is_valid_app_name(name):
    """filter out unwanted entries like categories and ratings"""
    if re.match(r'^\d+([,.]\d+)?$', name):
        return False
    
    # remove categorias e termos indesejados
    unwanted_terms = [
        "Apps e jogos", "Livros", "Jogos", "Filmes", "Música",
        "Notícias", "Educação", "Finanças", "Compras"
    ]
    
    return not any(unwanted_term.lower() in name.lower() for unwanted_term in unwanted_terms)

def is_valid_url(url):
    """Check if the input is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
    
def scrape_play_store(url):
    """main scraping function"""
    driver = setup_driver()
    
    try:
        driver.get(url)
        time.sleep(3 + random.random()*2)

        print("\nCarregando mais aplicativos...")
        for i in range(30):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8);")
            time.sleep(0.5 + random.random())
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5);")
            time.sleep(0.5 + random.random())
            print(f"Scroll {i+1}/30", end='\r')
        
        print("\nExtraindo nomes...")
        apps = []
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"], div.UVEnyf, div.VfPpkd-WsjYwc')
        
        for card in cards:
            try:
                name_elements = card.find_elements(By.CSS_SELECTOR, 'span, div > span, div.epHTyb, div.sT93pb')
                for element in name_elements:
                    name = element.text.strip()
                    if name and len(name) > 2 and is_valid_app_name(name):
                        apps.append(name)
                        break
            except:
                continue
        
        unique_apps = []
        seen = set()
        for app in apps:
            if app not in seen:
                seen.add(app)
                unique_apps.append(app)
                
        return unique_apps
        
    except Exception as e:
        return f"erro ao raspar dados: {str(e)}"
    finally:
        driver.quit()
        print("\nSessão do navegador encerrada")

if __name__ == "__main__":
    default_url = "https://play.google.com/store/search?q=servi%C3%A7os+profissionais&c=apps"
    
    while True:
        custom_url = input("\nCole aqui a URL da Play Store (ou Enter para usar a padrão): ").strip()
        
        if not custom_url:
            target_url = default_url
            break
        elif is_valid_url(custom_url):
            target_url = custom_url
            break
        else:
            print("\nerro... Isso não parece ser uma URL válida. Por favor, insira uma URL completa ou pressione Enter para usar a URL padrão.")

    print("\niniciando processo...")
    time.sleep(1)
    
    results = scrape_play_store(target_url)
    if isinstance(results, list):
        print(f"\nForam encontrados {len(results)} apps:")
        for i, app in enumerate(results[:100], 1): # limite a 100 para evitar sobrecarga de saída. pode ser ajustado
            print(f"{i:3d}. {app[:70] + '...' if len(app) > 70 else app}")
        
        with open("play_store_apps.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print(f"\nArquivo 'play_store_apps.txt' salvo com {len(results)} aplicativos.")
    else:
        print(f"\nErro: {results}")
    
    print("\nObs: uso apenas para fins de estudo.")