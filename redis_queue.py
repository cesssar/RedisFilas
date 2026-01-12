import redis
import json

class RedisQueue:


    def __init__(self, host='localhost', port=6379, db=0):
        self.__client = redis.Redis(
            host=host, 
            port=port, 
            db=db, 
            decode_responses=True
        )


    def enqueue(self, stream_name: str, data: dict):
        """Adiciona um item ao stream (XADD)."""
        return self.__client.xadd(stream_name, data)
    

    def create_group(self, stream_name: str, group_name: str):
        """Cria um grupo de consumidores se ele ainda não existir."""
        try:
            self.__client.xgroup_create(stream_name, group_name, id='0', mkstream=True)
        except redis.exceptions.ResponseError as e:
            if "already exists" not in str(e):
                raise e
            

    def dequeue(self, stream_name: str, group_name: str, consumer_name: str, timeout: int = 0):
        """
        Lê mensagens com auto-recuperação.
        Primeiro busca mensagens pendentes (não confirmadas) e depois mensagens novas.
        """
        
        # 1. Tenta recuperar mensagens que ficaram "presas" (já entregues mas sem ACK)
        # Usamos o ID '0' em vez de '>' para ler do histórico de pendentes do consumidor
        pending_result = self.__client.xreadgroup(
            groupname=group_name,
            consumername=consumer_name,
            streams={stream_name: '0'},
            count=1
        )

        # Se houver algo pendente, processa primeiro
        if pending_result and pending_result[0][1]:
            msg_id, data = pending_result[0][1][0]
            print(f" [!] Recuperando mensagem pendente: {msg_id}")
            return msg_id, data

        # 2. Se não houver pendentes, busca a próxima mensagem nova (ID '>')
        # o parâmetro consumername garante que uma mensagem pendente enviada para um worker chamado worker1
        # somente seja enviada novamente para o mesmo worker1 evitando auto-claim (roubo de tarefas)
        result = self.__client.xreadgroup(
            groupname=group_name,
            consumername=consumer_name,
            streams={stream_name: '>'},
            count=1,
            block=timeout
        )

        if result and result[0][1]:
            msg_id, data = result[0][1][0]
            return msg_id, data
            
        return None, None
    

    def acknowledge(self, stream_name: str, group_name: str, message_id: str):
        """Confirma o processamento da mensagem (ACK)."""
        return self.__client.xack(stream_name, group_name, message_id)
    


'''
implementar item abaixo no método dequeue após recuperar pendentes de outros workers
que estão há mais de x tempo sem confirmação
forma de evitar tarefas pendentes por worker morto
min_idle_time: Ele deve ser sempre maior do que o tempo máximo que sua tarefa leva para ser processada.

# 2. Segundo: Tenta "roubar" tarefas de outros workers que MORRERAM
        # Só pega tarefas que estão sem ACK há mais de 30.000ms (30 segundos)
        # Isso evita pegar tarefas de workers que ainda estão trabalhando, mas são lentos.
        claimed = self.__client.xautoclaim(
            name=stream_name,
            groupname=group_name,
            consumername=consumer_name,
            min_idle_time=30000, # 30 segundos de inatividade
            count=1
        )
        # xautoclaim retorna (next_start_id, [list_of_messages])
        if claimed[1]:
            msg_id, data = claimed[1][0]
            print(f" [!] Reivindicando tarefa órfã de outro worker: {msg_id}")
            return msg_id, data
'''