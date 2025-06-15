import time


# inicio = time.time()

# for i in range(100):
#      # Início da medição,

#      # Código a ser medido
#      soma = 0
#      for i in range(1, 1000001):
#           soma += i

#      # Fim da medição
#      fim = time.time()

#      # Calcula o tempo de execução
#      tempo_execucao = fim - inicio
#      print(f"Tempo de execução: {tempo_execucao:.4f} segundos")



  # Inicializa o temporizador
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

# Executa o código 100 vezes e mede o tempo de execução
for i in range(100):
    print(CapturarTempoExecucao(tempo))