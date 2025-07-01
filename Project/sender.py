import rethinkdb as r
from datetime import datetime
import pytz # Para lidar com fuso horário

# --- Configuração da Conexão ---
RDB_HOST = 'localhost'
RDB_PORT = 28015
CHAT_DB = 'chat_db'
CHAT_TABLE = 'mensagens'

# --- Conexão com o Banco ---
try:
    conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=CHAT_DB)
except r.errors.ReqlDriverError as e:
    print(f"Erro: Não foi possível conectar ao RethinkDB. Detalhes: {e}")
    exit(1)

# --- Loop Principal para Enviar Mensagens ---
print("Bem-vindo ao Chat Sender! Digite 'sair' para fechar.")
autor = input("Digite seu nome: ")

while True:
    texto = input(f"{autor}> ")

    if texto.lower() == 'sair':
        break

    if not texto: # Ignora mensagens vazias
        continue

    # Prepara o documento a ser inserido
    mensagem = {
        'autor': autor,
        'texto': texto,
        # Adiciona um timestamp com fuso horário
        'timestamp': datetime.now(pytz.utc)
    }

    # Insere o documento na tabela 'mensagens'
    r.table(CHAT_TABLE).insert(mensagem).run(conn)

print("Encerrando o sender...")
conn.close()