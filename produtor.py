from redis_queue import RedisQueue
from time import sleep

queue = RedisQueue()

STREAM = "tarefas"
GRUPO = "processar_ocorrencias"

queue.create_group(STREAM, GRUPO)

for i in range(1,51):
    # Gravando item
    print(f"Enviando tarefa: {i}")
    queue.enqueue(STREAM, {"id": i, "task": f"gravar ocorrência no AF {i*5065566}"})
    sleep(2)