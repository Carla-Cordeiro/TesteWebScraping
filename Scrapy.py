import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import datetime
import pytz
from selenium.common.exceptions import NoSuchElementException

# Inicialize o navegador do Chrome
navegador = webdriver.Chrome()


def abrir_site_linkedin():
    # Abra o LinkedIn
    navegador.get("https://www.linkedin.com")
    navegador.maximize_window()


def fechar_navegador(navegador):
    navegador.quit()


def selecionar_botao_vagas():
    botao_vagas = navegador.find_element(By.XPATH, '/html/body/nav/ul/li[4]')
    botao_vagas.click()
    sleep(3)


def preencher_campo_localizacao():
    campo_localizacao = navegador.find_element(By.XPATH, '//*[@id="job-search-bar-location"]')
    campo_localizacao.click()
    campo_localizacao.clear()
    campo_localizacao.send_keys("Brasil")
    sleep(3)

    item_localizacao = navegador.find_element(By.XPATH, '//*[@id="job-search-bar-location-typeahead-list"]/li[1]')
    item_localizacao.click()
    sleep(3)


def botao_tipo_vaga():
    tipo_vaga = navegador.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[4]/div/div/button')
    tipo_vaga.click()
    sleep(1)

    tempo_integral = navegador.find_element(By.XPATH, '//*[@id="f_JT-0"]')
    tempo_integral.click()
    sleep(1)

    botao_concluido = navegador.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[4]/div/div/div/button')
    botao_concluido.click()
    sleep(3)


def pegar_vagas():
    vagas = navegador.find_elements(By.XPATH, '//*[@id="main-content"]/section/ul/li')
    return vagas


def horario_atual():
    sp_tz = pytz.timezone('America/Sao_Paulo')
    sp_now = datetime.datetime.now(sp_tz)
    return sp_now.strftime("%H:%M %d/%m/%Y")


def imprimir_informacoes(urf_vaga, nome_vaga, nome_empresa, url_empresa, tipo_contratacao, nivel_exp,
                         numero_candidaturas, data_postagem_vaga, horario_scraping, local_empresa):
    print('================================================================================')
    print(f'url vaga: {urf_vaga}')
    print(f'nome_vaga: {nome_vaga}')
    print(f'nome_empresa: {nome_empresa}')
    print(f'url_empresa: {url_empresa}')
    print(f'tipo_contratacao: {tipo_contratacao}')
    print(f'nivel_exp: {nivel_exp}')
    print(f'numero_candidaturas: {numero_candidaturas}')
    print(f'data_postagem_vaga: {data_postagem_vaga}')
    print(f'horario_scraping: {horario_atual}')
    print(f'local_empresa: {local_empresa}')
    print('================================================================================')


def percorrer_vagas(vagas_lista):
    vaga_final = []
    for vaga in vaga_final:
        sleep(1.5)
        link_vaga = vaga.find_element(By.CSS_SELECTOR,
                                    '[data-tracking-control-name="public_jobs_jserp-result_search-card"]')
        url_vaga = link_vaga.get_attribute('href')

        navegador.execute_script("window.open('');")
        navegador.switch_to.window(navegador.window_handles[1])
        navegador.get(url_vaga)
        sleep(3)

        nome_vaga = navegador.find_element(By.XPATH,
                                           '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1')
        nome_empresa = navegador.find_element(By.XPATH,
                                              '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a')
        elemento = navegador.find_element(By.XPATH,
                                          '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a')
        url_empresa = elemento.get_attribute("href")

        # modelo_contratacao
        tipo_contratacao = navegador.find_element(By.XPATH,
                                                  '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[2]/span')
        nivel_exp = navegador.find_element(By.XPATH,
                                           '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[1]/span')

        numero_candidaturas = ''
        try:
            numero_candidaturas = navegador.find_element(By.XPATH,
                                                         '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[2]')
        except NoSuchElementException:
            try:
                numero_candidaturas = navegador.find_element(By.XPATH,
                                                             '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/figure/figcaption')
            except NoSuchElementException:
                numero_candidaturas = "Não foi encontrado o número de candidaturas"

        data_postagem_vaga = navegador.find_element(By.XPATH,
                                                    '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span')

        # informações da empresa (quantidade de funcionarios e local)
        # numero_empregados_empresa = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd')
        local_empresa = navegador.find_element(By.XPATH,
                                               '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]')

        horario_scraping = horario_atual
        vaga_final.append((url_vaga, nome_vaga.text.title(), nome_empresa.text, url_empresa, tipo_contratacao.text,
                           nivel_exp.text, numero_candidaturas.text, data_postagem_vaga.text, horario_scraping,
                           local_empresa.text))

        imprimir_informacoes(url_vaga, nome_vaga.text.title(), nome_empresa.text, url_empresa, tipo_contratacao.text,
                             nivel_exp.text, numero_candidaturas.text, data_postagem_vaga.text, horario_scraping,
                             local_empresa.text)
        sleep(1.5)

        navegador.close()
        navegador.switch_to.window(navegador.window_handles[0])

    return vaga_final


def salvar_csv(lista_vaga):
    with open('informacoes.csv', 'w', newline='', encoding='utf-8-sig') as arquivo_csv:
        writer = csv.writer(arquivo_csv, delimiter=';')

        writer.writerow(
            ['URL da vaga no linkedin', 'Nome da vaga', 'Nome da empresa contratante', 'URL da empresa contratante',
             'Tipo de contratação', 'Nível de experiência', 'Número de candidaturas para vaga',
             'Data da postagem da vaga',
             'Horário do scraping', 'Local da empresa'])
        for vaga in lista_vaga:
            writer.writerow(vaga)


def iniciar_scraping():
    abrir_site_linkedin()
    selecionar_botao_vagas()
    preencher_campo_localizacao()
    botao_tipo_vaga()
    vagas = pegar_vagas()
    vagas_lista_final = percorrer_vagas(vagas)
    salvar_csv(vagas_lista_final)

    fechar_navegador(navegador)


iniciar_scraping()