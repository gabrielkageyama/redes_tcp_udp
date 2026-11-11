import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORTA_TCP = 5000
PORTA_UDP = 5001
TAMANHO_BUFFER = 4096


def criar_resposta(mensagem):
    if not mensagem.startswith("/"):
        return f"[TCP] Mensagem recebida: {mensagem}", False

    agora = datetime.now()

    if mensagem == "/oi":
        return "[Chatbot] Olá! Como posso ajudar?", False
    if mensagem == "/hora":
        return f"[Chatbot] Agora são {agora.strftime('%H:%M')}.", False
    if mensagem == "/data":
        return f"[Chatbot] Hoje é {agora.strftime('%d/%m/%Y')}.", False
    if mensagem == "/sobre":
        return "[Chatbot] Sou um chatbot simples integrado ao servidor TCP.", False
    if mensagem == "/ajuda":
        comandos = "[Chatbot] Comandos: /oi, /hora, /data, /sobre, /ajuda e /sair."
        return comandos, False
    if mensagem == "/sair":
        return "[Chatbot] Conexão encerrada.", True

    return "[Chatbot] Comando desconhecido. Digite /ajuda.", False


def atender_cliente(conexao, endereco):
    ip_cliente, porta_cliente = endereco
    print(f"[TCP] Cliente conectado: {ip_cliente}:{porta_cliente}")

    try:
        with conexao, conexao.makefile("r", encoding="utf-8", newline="\n") as entrada:
            while True:
                linha = entrada.readline()

                if linha == "":
                    print(f"[TCP] Cliente desconectado: {ip_cliente}:{porta_cliente}")
                    break

                mensagem = linha.rstrip("\r\n")

                if not mensagem:
                    resposta = "[TCP] Mensagem vazia ignorada."
                    encerrar = False
                else:
                    print(
                        f"[TCP] Mensagem de {ip_cliente}:{porta_cliente}: {mensagem}"
                    )
                    resposta, encerrar = criar_resposta(mensagem)

                conexao.sendall((resposta + "\n").encode("utf-8"))

                if encerrar:
                    print(
                        f"[TCP] Conexão encerrada por {ip_cliente}:{porta_cliente}"
                    )
                    break
    except (ConnectionError, OSError, UnicodeError) as erro:
        print(f"[TCP] Erro com {ip_cliente}:{porta_cliente}: {erro}")


def receber_udp(evento_encerramento):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
            socket_udp.bind((HOST, PORTA_UDP))
            socket_udp.settimeout(1.0)
            print(f"[UDP] Aguardando mensagens na porta {PORTA_UDP}...")

            while not evento_encerramento.is_set():
                try:
                    dados, endereco = socket_udp.recvfrom(TAMANHO_BUFFER)
                except TimeoutError:
                    continue
                except OSError as erro:
                    if not evento_encerramento.is_set():
                        print(f"[UDP] Erro ao receber mensagem: {erro}")
                    break

                mensagem = dados.decode("utf-8", errors="replace")
                ip_remetente, porta_remetente = endereco
                print(f"[UDP] Mensagem recebida: {mensagem}")
                print(f"[UDP] Origem: {ip_remetente}:{porta_remetente}")
    except OSError as erro:
        print(f"[UDP] Não foi possível usar a porta {PORTA_UDP}: {erro}")


def iniciar_servidor():
    evento_encerramento = threading.Event()
    thread_udp = None

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
            socket_tcp.bind((HOST, PORTA_TCP))
            socket_tcp.listen()

            print("Servidor iniciado.")
            print(f"[TCP] Aguardando conexões na porta {PORTA_TCP}...")

            thread_udp = threading.Thread(
                target=receber_udp,
                args=(evento_encerramento,),
                daemon=True,
            )
            thread_udp.start()

            while True:
                conexao, endereco = socket_tcp.accept()
                atender_cliente(conexao, endereco)
                print(f"[TCP] Aguardando conexões na porta {PORTA_TCP}...")
    except KeyboardInterrupt:
        print("\nEncerramento solicitado pelo usuário.")
    except OSError as erro:
        print(f"[TCP] Não foi possível iniciar o servidor: {erro}")
    finally:
        evento_encerramento.set()
        if thread_udp is not None:
            thread_udp.join(timeout=2)
        print("Servidor encerrado.")


if __name__ == "__main__":
    iniciar_servidor()
