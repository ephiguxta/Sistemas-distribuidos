import socket, time
from ast import literal_eval

def mostrarMensagem(msg):
    # como o dado enviado é uma representação de lista em string e tem
    # alguns dados a mais no começo, devemos removêlos
    indiceList = msg.index('[')
    msg = msg[indiceList:]

    msg = literal_eval(msg)
    for char in msg:
        print(f"{char}", end="")

# Endereço IP e PORTA do servidor
# SERVER_IP = '10.25.2.154'
SERVER_IP = '0.0.0.0'
SERVER_PORTA = 9998

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_tcp.connect((SERVER_IP, SERVER_PORTA - 1))
print(cliente_tcp.recv(1024).decode())
tema = input("Digite o número do tema (1-3): ").strip()
cliente_tcp.send(tema.encode())
cliente.sendto("Iniciar".encode(), (SERVER_IP, SERVER_PORTA))

while True:
    data, _ = cliente.recvfrom(1024)
    mensagem = data.decode()
    mostrarMensagem(mensagem)
    letra = input("Letra: ").strip().lower()
    cliente.sendto(letra.encode(), (SERVER_IP, SERVER_PORTA))#o servidor não local é ('10.25.2.154', 9999)

