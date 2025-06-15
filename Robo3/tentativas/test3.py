from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

# Crie um novo arquivo Excel
workbook = Workbook()
sheet = workbook.active
sheet.title = "MinhaTabela"

# Insira os dados na planilha
dados = [
    ["Nome", "Idade", "Cidade"],
    ["Ana", 9999, "São Paulo"],
    ["Carlos", 9999, "Rio de Janeiro"],
    ["Beatriz", 9999, "Belo Horizonte"]
]

for linha in dados:
    sheet.append(linha)

# Defina o intervalo da tabela (com base nos dados adicionados)
intervalo_tabela = f"A1:C{len(dados)}"
tabela = Table(displayName="TabelaExemplo", ref=intervalo_tabela)

# Estilo da tabela
estilo = TableStyleInfo(
    name="TableStyleMedium9",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=True
)
tabela.tableStyleInfo = estilo

# Adicione a tabela à planilha
sheet.add_table(tabela)

# Salve o arquivo Excel
workbook.save("arquivo_tabela.xlsx")
print("Tabela criada com sucesso!")