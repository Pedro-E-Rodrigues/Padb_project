import rethinkdb as r
import time

# --- Configuração da Conexão ---
# Se o RethinkDB estiver em outra máquina, mude o host.
RDB_HOST = 'localhost'
RDB_PORT = 28015
CHAT_DB = 'chat_db'
CHAT_TABLE = 'mensagens'

print("Iniciando o listener de mensagens...")

# --- Conexão com o Banco ---
# O 'try...except' garante que o script avise se não conseguir conectar.
try:
    conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=CHAT_DB)
except r.errors.ReqlDriverError as e:
    print(f"Erro: Não foi possível conectar ao RethinkDB. Verifique se o contêiner Docker está rodando. Detalhes: {e}")
    exit(1)

print("Conectado ao RethinkDB. Aguardando novas mensagens...")
print("--------------------------------------------------")

# --- O Coração do Listener ---
# r.table('mensagens').changes() é o comando mágico.
# Ele cria um 'feed' que recebe atualizações em tempo real da tabela.
feed = r.table(CHAT_TABLE).changes().run(conn)

# O loop 'for' fica aqui, bloqueado, esperando o 'feed' enviar algo.
for nova_mensagem in feed:
    # 'nova_mensagem' é um dicionário. A mensagem real está em 'new_val'.
    if nova_mensagem and nova_mensagem.get('new_val'):
        msg = nova_mensagem['new_val']
        # Formata o timestamp para um formato legível
        timestamp = msg['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
        print(f"[{timestamp}] {msg['autor']}: {msg['texto']}")