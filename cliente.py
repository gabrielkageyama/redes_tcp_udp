import socket

# Altere estes endereços para realizar testes em outra máquina ou sub-rede.
HOST = "127.0.0.1"
BROADCAST = "255.255.255.255"
PORTA_TCP = 5000
PORTA_UDP = 5001


def enviar_udp(mensagem):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
            socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            socket_udp.sendto(mensagem.encode("utf-8"), (BROADCAST, PORTA_UDP))
        print("[UDP] Mensagem enviada.")
    except OSError as erro:
        print(f"[UDP] Falha ao enviar mensagem: {erro}")


def iniciar_cliente():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
            socket_tcp.connect((HOST, PORTA_TCP))
            print(f"Conectado ao servidor TCP em {HOST}:{PORTA_TCP}!")
            print("Digite /ajuda para visualizar os comandos.\n")

            with socket_tcp.makefile("r", encoding="utf-8", newline="\n") as respostas:
                while True:
                    try:
                        mensagem = input("> ").strip()
                    except EOFError:
                        print("\nEntrada encerrada pelo usuário.")
                        break

                    if not mensagem:
                        print("Digite uma mensagem.")
                        continue

                    if mensagem == "/udp" or mensagem.startswith("/udp "):
                        conteudo_udp = mensagem[4:].strip()
                        if not conteudo_udp:
                            print("[UDP] Informe uma mensagem após /udp.")
                            continue

                        enviar_udp(conteudo_udp)
                        continue

                    socket_tcp.sendall((mensagem + "\n").encode("utf-8"))
                    resposta = respostas.readline()

                    if resposta == "":
                        print("[TCP] O servidor encerrou a conexão inesperadamente.")
                        break

                    print(resposta.rstrip("\r\n"))

                    if mensagem == "/sair":
                        break
    except KeyboardInterrupt:
        print("\nConexão encerrada pelo usuário.")
    except ConnectionRefusedError:
        print(f"[TCP] Não foi possível conectar a {HOST}:{PORTA_TCP}.")
    except (ConnectionError, OSError, UnicodeError) as erro:
        print(f"[TCP] Erro de comunicação: {erro}")


if __name__ == "__main__":
    iniciar_cliente()
