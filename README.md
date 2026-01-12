# Redis como gerenciador de filas — Exemplo ✅

Este repositório é um **exemplo prático** de uso do Redis (Streams) como sistema de gestão de filas, com produtores e múltiplos workers em Python.

---

## 🧰 Tecnologias usadas

- **Redis** (Streams & Consumer Groups)
- **Docker** e **docker-compose** (para subir o Redis localmente)
- **Python 3.8+**
- Biblioteca Python: `redis` (veja `requirements.txt`)

---

## 🗂 Estrutura do projeto

- `docker-compose.yaml` — definindo serviços Redis e RedisInsight
- `produtor.py` — script que envia tarefas para o stream
- `worker_1.py` / `worker_2.py` — workers que consomem e processam tarefas
- `redis_queue.py` — wrapper simples para operações de Streams (enqueue, dequeue, ack)
- `requirements.txt` — dependências Python

---

## 🚀 Como subir os containers (Docker)

1. Certifique-se de ter o Docker e o docker-compose instalados.
2. Na raiz do projeto, execute:

```bash
docker-compose up -d
```

3. Verifique se os serviços subiram:

```bash
docker-compose ps
```

O `docker-compose.yaml` expõe o Redis na porta `6379` e o RedisInsight em `5540`.

---

## 🐍 Preparar ambiente Python e instalar dependências

1. Crie e ative um ambiente virtual (Windows):

PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

CMD:
```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como testar os scripts Python

1. Em terminais separados, execute os workers:

```bash
python worker_1.py
python worker_2.py
```

Você verá mensagens como `Aguardando mensagens em tarefas...`.

2. Em outro terminal, execute o produtor para enviar tarefas:

```bash
python produtor.py
```

O `produtor.py` envia 50 tarefas para o stream `tarefas` e cada worker irá consumir/processar e confirmar (ACK) as mensagens.

Observações:
- O `stream` usado é **`tarefas`** e o `consumer group` é **`processar_ocorrencias`**.
- Cada worker é identificado por um nome (`worker_1`, `worker_2`); o código demonstra como simular um erro (quando `id == 20`) para testar recuperação de mensagens pendentes.

---

## 🛠️ Dicas e resolução de problemas

- Se o Python não conectar ao Redis, verifique se o container está rodando e a porta `6379` está exposta.
- Use o RedisInsight (porta `5540`) para inspecionar streams, grupos, e mensagens pendentes.
- Para limpar tudo (containers + volumes):

```bash
docker-compose down -v
```

---

## 🔍 Usando RedisInsight para visualizar dados

1. Abra o navegador e acesse `http://localhost:5540`.
2. Conecte ao Redis (host: `localhost`, porta: `6379`).
3. Na aba **Streams**, selecione o stream `tarefas` para visualizar:
    - Todas as mensagens enfileiradas
    - IDs das mensagens e seus conteúdos
4. Na aba **Consumer Groups**, selecione `processar_ocorrencias` para inspecionar:
    - Mensagens pendentes (não confirmadas)
    - Última mensagem entregue a cada consumer
    - Status de cada worker (`worker_1`, `worker_2`)
5. Use a aba **CLI** para executar comandos Redis manualmente, como:
    ```
    XLEN tarefas
    XINFO GROUPS tarefas
    XPENDING tarefas processar_ocorrencias
    ```

![Painel RedisInsight](https://github.com/cesssar/RedisFilas/blob/main/redis_filas.gif)

Licença: MIT (sinta-se livre para adaptar este material para estudos ou testes).