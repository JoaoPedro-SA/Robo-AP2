import pandas as pd

# Cria o DataFrame com valores de exemplo
df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6],
    "C": [7, 8, 9]
})

# Salva o DataFrame em um arquivo CSV
df.to_csv("output.csv", index=False, sep=",")
print("Arquivo CSV salvo com sucesso!")

# Lê o arquivo CSV para garantir que os dados foram salvos corretamente
df_csv = pd.read_csv("output.csv")
print(df_csv)

# Transforma o CSV em um arquivo Excel
df_csv.to_excel("output.xlsx", index=False)
print("Arquivo Excel salvo com sucesso!")