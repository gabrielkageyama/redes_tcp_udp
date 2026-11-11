# Aplicação integrada de redes

Aplicação acadêmica cliente-servidor em Python que demonstra comunicação TCP,
UDP Broadcast e um chatbot com comandos predefinidos. Toda a interação ocorre
pelo terminal, usando um único cliente e um único servidor.

## Funcionalidades

- **TCP:** mantém uma conexão entre cliente e servidor, envia mensagens e recebe
  uma confirmação para cada mensagem.
- **UDP Broadcast:** o cliente envia um datagrama para a rede por meio do comando
  `/udp`. O envio não garante que algum destinatário receberá a mensagem.
- **Chatbot:** o servidor interpreta comandos enviados pela conexão TCP e gera
  respostas simples de data, hora, ajuda e apresentação.

O servidor recebe TCP e UDP ao mesmo tempo. O receptor UDP é executado em uma
thread, enquanto a thread principal atende as conexões TCP sequencialmente.

## Estrutura

```text
redes_tcp_udp/
├── evidencias/
│   ├── tcp.pcapng
│   ├── udp.pcapng
│   └── ...
├── servidor.py
├── cliente.py
├── README.md
└── RELATORIO.md
```

O PDF é o documento de referência fornecido para a atividade e não faz parte da
execução da aplicação.

## Requisitos

- Python 3 instalado;
- dois terminais do Windows PowerShell;
- permissão no firewall para as portas TCP `5000` e UDP `5001` nos testes em
  rede local.

Não há dependências externas.

## Como executar

Abra o primeiro PowerShell na pasta do projeto e inicie o servidor:

```powershell
python servidor.py
```

O servidor escuta TCP em `0.0.0.0:5000` e UDP em `0.0.0.0:5001`.

Abra um segundo PowerShell na mesma pasta e inicie o cliente:

```powershell
python cliente.py
```

Por padrão, o cliente se conecta a `127.0.0.1:5000`.

## Comandos

| Comando | Função |
|---|---|
| `/oi` | Exibe uma saudação. |
| `/hora` | Exibe o horário atual do servidor. |
| `/data` | Exibe a data atual do servidor. |
| `/sobre` | Descreve o chatbot. |
| `/ajuda` | Lista os comandos disponíveis. |
| `/udp mensagem` | Envia `mensagem` por UDP Broadcast. |
| `/sair` | Encerra a conexão TCP do cliente. |

Qualquer texto que não começa com `/` é enviado normalmente por TCP. Um comando
desconhecido recebe uma orientação para usar `/ajuda`. O comando `/udp` é
processado apenas pelo cliente e não é enviado ao chatbot.

## Exemplo de uso

```text
> Olá servidor
[TCP] Mensagem recebida: Olá servidor

> /oi
[Chatbot] Olá! Como posso ajudar?

> /hora
[Chatbot] Agora são 19:45.

> /udp Teste de broadcast
[UDP] Mensagem enviada.

> /sair
[Chatbot] Conexão encerrada.
```

A confirmação de envio UDP informa apenas que a operação local foi executada
sem erro. Ela não confirma o recebimento do datagrama.

## Alteração dos endereços IP

As configurações ficam no início de `cliente.py`:

```python
HOST = "127.0.0.1"
BROADCAST = "255.255.255.255"
```

- `HOST` deve receber o IPv4 da máquina que executa `servidor.py` quando cliente
  e servidor estiverem em computadores diferentes.
- `BROADCAST` pode precisar ser substituído pelo endereço de broadcast da
  sub-rede, como `192.168.1.255`. Consulte a configuração da rede local.

As portas também estão declaradas como constantes no início dos dois arquivos.
Se forem alteradas, os valores do cliente e do servidor devem permanecer iguais.

## Teste entre computadores

1. Conecte os dois computadores à mesma rede local.
2. No computador servidor, descubra o endereço IPv4 com `ipconfig`.
3. Permita, se necessário, o Python ou as portas `5000/TCP` e `5001/UDP` no
   Firewall do Windows.
4. No `cliente.py`, altere `HOST` para o IPv4 do servidor.
5. Ajuste `BROADCAST` para o broadcast da sub-rede se `255.255.255.255` não for
   aceito pela rede.
6. Execute primeiro `python servidor.py` e depois `python cliente.py`.
7. Teste uma mensagem comum, os comandos do chatbot e `/udp mensagem`.

Roteadores, redes Wi-Fi com isolamento de clientes, máquinas virtuais e regras
de firewall podem bloquear UDP Broadcast. Por isso, um envio bem-sucedido no
cliente pode não aparecer no servidor. O UDP usado aqui não possui confirmação,
retransmissão nem garantia de entrega.

O atendimento TCP é intencionalmente sequencial: o servidor atende um cliente
por vez e volta a aceitar novas conexões após a desconexão atual.

## Encerramento

No cliente, digite `/sair` para encerrar a conexão de forma organizada. Também é
possível usar `Ctrl+C`. No terminal do servidor, use `Ctrl+C` para fechar o
servidor TCP e solicitar o encerramento do receptor UDP.

O relatório da atividade está disponível em `RELATORIO.md`. As capturas de
tela e os arquivos de captura TCP e UDP do Wireshark estão disponíveis na pasta
`evidencias/`.
