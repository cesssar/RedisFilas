from redis_queue import RedisQueue
from time import sleep
import sys

queue = RedisQueue()

STREAM = "tarefas"
GRUPO = "processar_ocorrencias"

# Obtém consumer_name do argumento ou usa padrão
if len(sys.argv) > 1:
    CONSUMER_NAME = sys.argv[1]
else:
    print("Uso: python worker.py <consumer_name>")
    print("Exemplo: python worker.py worker_1")
    sys.exit(1)

queue.create_group(STREAM, GRUPO)

print(f"Aguardando mensagens em {STREAM}...")
print(f"Consumidor: {CONSUMER_NAME}")

while True:

    msg_id, task = queue.dequeue(STREAM, GRUPO, CONSUMER_NAME) 

    if task:
        try:
            print(f"Processando: {task}")
            # ... sua lógica de negócio aqui ...
            if task['id'] == 20:
                raise Exception('Simulando erro')           
            # enviar confirmação para que o Redis remova o item da fila
            queue.acknowledge(STREAM, GRUPO, msg_id)
            queue.delete(STREAM, msg_id)
            print(f"✓ Tarefa {task['id']} concluída e deletada")
        except Exception as e:
            print(f"Erro ao processar. A mensagem {msg_id} continua salva no Redis.")


    sleep(2)