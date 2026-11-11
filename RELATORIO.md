# Relatório — Atividade Prática de Redes de Computadores

## 1. Objetivo

Desenvolver uma aplicação em Python para demonstrar comunicação TCP, UDP Broadcast e um chatbot por sockets, relacionando seu funcionamento aos conceitos da camada de transporte.

## 2. Implementação

O projeto utiliza dois programas: `servidor.py` e `cliente.py`. As mensagens comuns e os comandos do chatbot utilizam **TCP na porta 5000**. O comando `/udp mensagem` envia um **datagrama UDP Broadcast para a porta 5001**, recebido por uma thread no servidor. A aplicação funciona pelo terminal e utiliza apenas bibliotecas nativas do Python.

## 3. Testes e resultados

Os resultados abaixo correspondem aos testes locais e aos testes realizados entre dois computadores conectados à mesma rede.

| Teste | Resultado |
|---|---|
| Conexão TCP | Cliente conectou ao servidor local. |
| Mensagens TCP | Servidor recebeu mensagens e respondeu. |
| Falha de conexão | Com o servidor desligado, o cliente informou a falha. |
| UDP Broadcast | O datagrama foi enviado e recebido no ambiente local de teste; falta validar na rede utilizada na apresentação. |
| Chatbot | `/oi`, `/hora`, `/data`, `/sobre` e `/ajuda` responderam; comando desconhecido também foi tratado. |
| Encerramento | `/sair` encerrou a conexão e o servidor aceitou outra conexão. |
| Wireshark | Capturas e analises TCP e UDP com conexão em dois computadores na mesma rede. |

**Evidências:**
- [Handshake TCP](evidencias/handshake-tcp.png)
- [ACKs e janela TCP](evidencias/ack-janela-tcp.png)
- [Dados da comunicação TCP](evidencias/dados-tcp.png)
- [Filtro de retransmissões](evidencias/retransmissoes-tcp%20%28nada%20identificado%29.png)
- [Pacote UDP Broadcast](evidencias/udp-pacote.png)
- [Terminal do cliente UDP](evidencias/udp-terminal-cliente.jpeg)
- [Terminal do servidor UDP](evidencias/udp-terminal-servidor.png)
- [Teste do chatbot](evidencias/chatbot.jpeg)
- [Falha de conexão](evidencias/falha-conexao.png)


## 4. Questões para análise

**1. Qual a diferença entre TCP e UDP?**  
TCP estabelece uma conexão e oferece entrega confiável e ordenada de bytes. UDP envia datagramas sem estabelecer conexão e sem garantir sua entrega ou ordem.

**2. Por que o TCP é considerado confiável?**  
Porque usa numeração de sequência, confirmações (ACKs), verificações de integridade e retransmissões para lidar com perdas e manter a ordem dos dados.

**3. Como funciona o controle de erros no TCP?**  
O TCP detecta possíveis corrupções pelo checksum e usa números de sequência, ACKs e retransmissões para recuperar dados perdidos e tratar duplicações.

**4. Qual a finalidade do controle de fluxo?**  
Evitar que o emissor envie dados mais rapidamente do que o receptor consegue processar, utilizando a janela de recepção anunciada.

**5. O que significa congestionamento de rede?**  
Ocorre quando a demanda de tráfego excede a capacidade de processamento ou transmissão da rede, podendo gerar atrasos e perdas. O TCP possui mecanismos para ajustar a taxa de envio.

**6. Como os sockets permitem a comunicação entre aplicações?**  
Sockets são interfaces oferecidas pelo sistema operacional para que aplicações enviem e recebam dados pela rede, utilizando protocolos como TCP e UDP e endereços IP e portas.

**7. Qual a vantagem e a limitação do UDP Broadcast?**  
Permite enviar um datagrama para vários dispositivos da rede local sem abrir conexões individuais. Porém, não garante entrega e geralmente não atravessa roteadores.

**8. Qual protocolo foi escolhido para o chatbot e por quê?**  
Foi escolhido TCP, pois as perguntas e respostas se beneficiam de uma conexão e da entrega ordenada e confiável dos dados.

**9. Quais problemas ocorreram na implementação?**  
O tratamento de desconexões; Restrições de firewall e broadcast entre computadores dificultou os testes; Adaptação com a ferramenta Wireshark.

**10. O que foi observado no Wireshark?**  
No Wireshark, foi possível observar o estabelecimento da conexão TCP por meio do *three-way handshake* (SYN, SYN-ACK e ACK), a troca de mensagens entre cliente e servidor e os pacotes de confirmação (ACK), incluindo informações da janela TCP relacionadas ao controle de fluxo. Não foram identificadas retransmissões durante os testes.

Os ACKs e os números de sequência observados estão relacionados ao controle de erros do TCP, enquanto a janela anunciada está relacionada ao controle de fluxo. Como não foram observadas retransmissões, perdas ou atrasos significativos na captura, não foram identificados sinais de congestionamento durante o teste. Isso não significa que o TCP não possua controle de congestionamento, mas apenas que não houve condições suficientes para acioná-lo de forma perceptível no cenário testado.

Na comunicação UDP Broadcast, foi identificado um datagrama enviado do IP `192.168.1.82` para o endereço de broadcast `192.168.1.255`, utilizando a porta de destino `5001`. O recebimento foi confirmado no terminal do servidor.

## 5. Conclusão

A implementação demonstra o uso de TCP para troca de mensagens e chatbot e de UDP para envio em broadcast. O TCP oferece mecanismos de confiabilidade e controle de fluxo, enquanto o UDP é mais simples e não garante a entrega. A análise prática no Wireshark complementou a atividade ao permitir observar o funcionamento desses protocolos nos pacotes capturados.
