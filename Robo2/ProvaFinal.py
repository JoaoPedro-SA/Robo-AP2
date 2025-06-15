import re
import sqlite3
import time
import requests
import pyautogui

email = input("Digite o e-mail de destino para o relatório: ")
# =========================
# CONFIGURAÇÕES
# =========================

DATABASE = 'projeto_rpa.db'
URL_API = "https://rickandmortyapi.com/api/character"
EMAIL_DESTINO = email

# =========================
# PARTE 1: API Rick and Morty
# =========================

def confirmar_uso_requests():
    try:
        import requests
        return True, f"Usando requests versão: {requests.__version__}"
    except ImportError:
        return False, "Módulo requests NÃO está disponível."

def justificar_escolha_api():
    return (
        "Escolhi a API Rick and Morty por ser pública, fácil de usar e divertida, "
        "oferecendo dados interessantes para praticar requisições HTTP, JSON e armazenamento em SQLite."
    )

def coletar_personagens():
    try:
        resposta = requests.get(URL_API, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()['results']
        return [
            {'id': p['id'], 'nome': p['name'], 'especie': p['species'], 'status': p['status']}
            for p in dados
        ]
    except Exception as e:
        print(f"Erro ao coletar personagens: {e}")
        return []

# =========================
# PARTE 2: Banco de Dados
# =========================

def salvar_personagens(personagens):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS personagens (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            especie TEXT,
            status TEXT
        )
    ''')
    for p in personagens:
        c.execute('''
            INSERT OR REPLACE INTO personagens (id, nome, especie, status)
            VALUES (?, ?, ?, ?)
        ''', (p['id'], p['nome'], p['especie'], p['status']))
    conn.commit()
    conn.close()

# =========================
# PARTE 3: Regex
# =========================

def filtrar_aliens_com_regex():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT id, nome, especie, status FROM personagens')
    personagens = c.fetchall()

    c.execute('''
        CREATE TABLE IF NOT EXISTS dados_processados (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            especie TEXT,
            status TEXT
        )
    ''')

    padrao = re.compile(r'^alien$', re.IGNORECASE)

    for p in personagens:
        if padrao.match(p[2]):
            c.execute('''
                INSERT OR REPLACE INTO dados_processados (id, nome, especie, status)
                VALUES (?, ?, ?, ?)
            ''', (p[0], p[1], p[2], p[3]))

    conn.commit()
    conn.close()

# =========================
# PARTE 4: Relatório
# =========================

def gerar_relatorio():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM personagens')
    total_personagens = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM dados_processados')
    total_aliens = c.fetchone()[0]

    c.execute('SELECT id, nome, especie, status FROM personagens')
    personagens = c.fetchall()

    conn.close()

    linhas = [
        f"{'ID':<5} {'Nome':<30} {'Espécie':<20} {'Status':<10}",
        "-" * 70
    ]
    for p in personagens:
        linhas.append(f"{p[0]:<5} {p[1]:<30} {p[2]:<20} {p[3]:<10}")

    relatorio = (
        "\n===== RELATÓRIO DE PERSONAGENS (RICK AND MORTY) =====\n\n"
        f"API utilizada: {URL_API}\n"
        f"Total de personagens coletados: {total_personagens}\n"
        f"Total de Aliens identificados com Regex: {total_aliens}\n"
        f"Justificativa da escolha da API: {justificar_escolha_api()}\n\n"
        "Lista de Personagens:\n\n" +
        "\n".join(linhas)
    )
    return relatorio

# =========================
# PARTE 5: Enviar e-mail com PyAutoGUI
# =========================

def enviar_email_automatico(mensagem):
    print("Por favor, não mexa no mouse ou teclado durante a execução.")

    time.sleep(5)  # Tempo para o usuário se preparar
    pyautogui.press("win")
    time.sleep(5)
    pyautogui.typewrite("google chrome")
    time.sleep(5)
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.hotkey("ctrl", "l")  # Focar na barra de endereços

    pyautogui.write("https://mail.google.com")
    pyautogui.press("enter")
    time.sleep(10)

    pyautogui.press("left")
    pyautogui.press("up")
    pyautogui.press("enter")

    time.sleep(5)
    pyautogui.write(EMAIL_DESTINO)
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.press("tab")
    time.sleep(2)
    pyautogui.write("Relatório Final - RPA")
    time.sleep(5)
    pyautogui.press("tab")
    pyautogui.write(mensagem)
    time.sleep(10)
    pyautogui.press("tab")
    pyautogui.hotkey("enter")  # Enviar o e-mail

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

def main():
    print("\n=========== PROVA FINAL DE RPA ===========\n")

    print("1 - Verificando biblioteca requests...")
    ok, msg = confirmar_uso_requests()
    print(msg)
    if not ok:
        return

    print("\n2 - Coletando personagens da API...")
    personagens = coletar_personagens()
    print(f"Total coletado: {len(personagens)}")

    print("\n3 - Salvando personagens no banco de dados...")
    salvar_personagens(personagens)

    print("\n4 - Filtrando aliens com Regex...")
    filtrar_aliens_com_regex()

    print("\n5 - Gerando relatório final...")
    relatorio = gerar_relatorio()
    print(relatorio)

    print("\n6 - Enviando relatório por e-mail...")
    enviar_email_automatico(relatorio)

    print("\n=========== PROVA FINAL FINALIZADA ===========\n")

if __name__ == "__main__":
    main()
