from redis_queue import RedisQueue
from time import sleep

queue = RedisQueue()

STREAM = "tarefas"
GRUPO = "processar_ocorrencias"

queue.create_group(STREAM, GRUPO)

print(f"Aguardando mensagens em {STREAM}...")

while True:

    # worker_1 é o nome do consumidor, podem ter vários workers
    # Redis Stream não entrega o mesmo item para outro worker
    msg_id, task = queue.dequeue(STREAM, GRUPO, "worker_1") 

    if task:
        try:
            print(f"Processando: {task}")
            # ... sua lógica de negócio aqui ...
            if task['id'] == 20:
                raise Exception('Simulando erro')           
            # enviar confirmação para que o Redis remova o item da fila
            queue.acknowledge(STREAM, GRUPO, msg_id)
        except Exception as e:
            print(f"Erro ao processar. A mensagem {msg_id} continua salva no Redis.")


    sleep(2)