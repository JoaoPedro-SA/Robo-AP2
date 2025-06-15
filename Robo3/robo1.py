# %%
import pyautogui
import time
import pandas as pd 
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

inicio = time.time()
arquivo = "comandos.csv"
tabelaDados = pd.read_csv(arquivo, sep=",")
colunas = tabelaDados.columns
RegistroDeAcoes = []
novaColuna = ["tarefa realizada","status", "tempo estimado de execução"]
RegistroDeAcoes.append(novaColuna)


def RelatorioDeAcao(tarefa,status,tempoEstimadoDeExecucao):

     listaDeDados = [tarefa,status,tempoEstimadoDeExecucao]

     RegistarDadosDoRelatoriorio(listaDeDados)

def RegistarDadosDoRelatoriorio(DadosAnhados):
     RegistroDeAcoes.append(DadosAnhados)


def posicaoDaColuna(coluna,PegaNomeDaColuna):
     posicao = list(coluna).index(PegaNomeDaColuna)
     return posicao



def inicializaTemporizador():
     tempo = time.time()
     return tempo

tempo = inicializaTemporizador()

def CapturarTempoExecucao(tempo):
    inicio =  tempo 

    soma = 0
    for i in range(1, 1000001):
        soma += i

    fim = time.time()  
    tempo_execucao = fim - inicio
    tempoExecucaoFormatado = f"{tempo_execucao:.2f} segundos"
    return tempoExecucaoFormatado



def apertaButton(dado):
     pyautogui.press(dado)

def capturarDadoDeAcao(tabelaDados,linha,coluna):
    dado = tabelaDados.iloc[linha, coluna]
    return str(dado)


def digitaTexto(dado):
    pyautogui.write(dado)


def acao(tarefa, tipoAcao, acao):
     Status = True
     if tipoAcao == "Pausa":
          try:
               tempo_pausa = float(acao)  
               print(f"Pausando por {tempo_pausa} segundos...")
               Status = "Executado com sucesso"
               RelatorioDeAcao(tarefa, Status, CapturarTempoExecucao(tempo))
               return "Pausa"
          except ValueError:
               Status = f"Erro ao executar a ação: {acao}"
               RelatorioDeAcao(tarefa, Status, CapturarTempoExecucao(tempo))
               Status = False
               print(f"Erro: O valor '{acao}' para pausa não é um número válido.")
          

     elif tipoAcao == "tecla":
        time.sleep(1)
        if acao not in pyautogui.KEYBOARD_KEYS:  
            Status = False
            print(f"Erro: A tecla '{acao}' não é válida.")
        else:
            try:
                apertaButton(acao)
            except Exception as erro:  
                Status = False
                print(f"Erro ao apertar a tecla '{acao}': ", erro)

     elif tipoAcao == "texto":
        time.sleep(1)
        digitaTexto(str(acao))
     
     elif tipoAcao == "3click":
            time.sleep(1)
            try:
               print("estou clicando")
               pyautogui.click(clicks=3)
               print("estou clicando")
               pyautogui.click(clicks=3)
               print("estou clicando")
               pyautogui.click(clicks=3) 
            except Exception as erro:
                Status = False

     elif tipoAcao == "2teclas":
          time.sleep(1)
          try:
               teclas = acao.split()  
               pyautogui.hotkey(*teclas)  
          except Exception as erro:
               Status = False
               print(f"Erro ao apertar as teclas '{acao}': ", erro)
     
     elif tipoAcao == "pressionar":
          try:
               print(f"Pressionando a tecla '{acao}' por 3 segundos...")
               pyautogui.keyDown(acao)  
               pyautogui.keyUp(acao)  
               print(f"Tecla '{acao}' liberada.")
          except Exception as erro:
               Status = False
               print(f"Erro ao pressionar a tecla '{acao}': {erro}")
     elif tipoAcao == "mouseCentro":
          try:
               largura, altura = pyautogui.size()  # Obtém o tamanho da tela
               centro_x, centro_y = largura // 2, altura // 2  # Calcula o centro
               pyautogui.moveTo(centro_x, centro_y)  # Move o mouse para o centro
               print(f"Mouse movido para o centro da tela: ({centro_x}, {centro_y})")
          except Exception as erro:
               Status = False
               print(f"Erro ao mover o mouse para o centro: {erro}")
                              
     if Status:
          Status = "Executado com sucesso"
          RelatorioDeAcao(tarefa, Status, CapturarTempoExecucao(tempo))
          return False
     else:
          Status = f"Erro ao executar a ação: {acao}"
          RelatorioDeAcao(tarefa, Status, CapturarTempoExecucao(tempo))
          return True
     


def PassarOsDadosDoRelatorioParaExcel(ListaDeTabela): 

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "RelatorioDeExeculcao"


    for linha in ListaDeTabela:
        if isinstance(linha, (list, tuple)):  
            sheet.append(linha)
        else:
            print(f"Linha inválida ignorada: {linha}")

    for col in sheet.columns:
        max_length = 0
        col_letter = col[0].column_letter 
        for cell in col:
            try:
                if cell.value:  
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = max_length + 2  
        sheet.column_dimensions[col_letter].width = adjusted_width

    intervalo_tabela = f"A1:C{len(ListaDeTabela)}"
    tabela = Table(displayName="TabelaExemplo", ref=intervalo_tabela)


    estilo = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=True
    )
    tabela.tableStyleInfo = estilo


    sheet.add_table(tabela)

    workbook.save("RelatorioDeExeculcao.xlsx")
    print("Tabela criada com sucesso!")




DeuErro = False
for linha in range(0, len(tabelaDados)):

     RegistroDeAcoes = [list(novaColuna)] + RegistroDeAcoes[1:]  

     PassarOsDadosDoRelatorioParaExcel(RegistroDeAcoes)

    

     DeuErro = acao(
        capturarDadoDeAcao(tabelaDados, linha, posicaoDaColuna(colunas, "tarefa")),
        capturarDadoDeAcao(tabelaDados, linha, posicaoDaColuna(colunas, "tipo")),
        capturarDadoDeAcao(tabelaDados, linha, posicaoDaColuna(colunas, "dado"))
    )


     if DeuErro == "Pausa":
        try:
            tempo_pausa = float(tabelaDados.iloc[linha, posicaoDaColuna(colunas, "dado")])  
            print(f"Pausando por {tempo_pausa} segundos...")
            time.sleep(tempo_pausa)  
        except ValueError:
            print(f"Erro: O valor '{tabelaDados.iloc[linha, posicaoDaColuna(colunas, 'dado')]}' não é um número válido para pausa.")
        DeuErro = False 
     
     if DeuErro == True:
          break
     

RegistroDeAcoes = [list(novaColuna)] + RegistroDeAcoes[1:]  

PassarOsDadosDoRelatorioParaExcel(RegistroDeAcoes)





