import csv
from playwright.sync_api import Playwright, sync_playwright

url = ['https://sistemaswebb3-listados.b3.com.br/fundsPage/34',
       'https://sistemaswebb3-listados.b3.com.br/fundsPage/27',
       'https://sistemaswebb3-listados.b3.com.br/fundsPage/7']

 
def run(playwright: Playwright, url: str) -> None:
    def handle_response(response):
        if ("fundsProxy/fundsCall/GetDetailFundSIG" in response.url
            or "fundsProxy/fundsCall/GetListedSupplementFunds" in response.url):
            with open("raw/fii_urls.txt", 'a') as f:
                f.write(f"{response.url}\n")

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.on('response', handle_response)
    page.goto(url, wait_until="networkidle")

    # Download CSV
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Exportar lista completa de Fundos em CSV").click()
    
    download = download_info.value
    with open(download.path()) as csvfile:
        r = csv.reader(csvfile, delimiter=';')
        names = [line[-2].strip() for line in r if len(line) > 1]
        names = names[1:]

    for name in names:
        name = name.strip()
        try:
            page.get_by_placeholder("Digite o assunto desejado").fill(name)
            page.get_by_placeholder("Digite o assunto desejado").press("Enter")
            page.wait_for_load_state("networkidle") 
            
            page.get_by_role('heading', name=name).click(timeout=60*1000)
            page.get_by_role("link", name="Eventos Corporativos").click()
            page.wait_for_load_state("networkidle") 
            
            page.get_by_role("button", name="Voltar").click()
            page.get_by_role("button", name="Voltar").click()
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"{name} ERROR:\n{e}")
            page.goto(url, wait_until="networkidle")

    # ---------------------
    context.close()
    browser.close()


for u in url:
    with sync_playwright() as playwright:
        run(playwright, u)
