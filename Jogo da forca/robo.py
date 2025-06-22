import socket 
import random

# Endereço IP e PORTA do servidor
# SERVER_IP = '10.25.2.154'
SERVER_IP = '0.0.0.0'
SERVER_PORTA = 9998

# Palavras por categoria
animal = [['c', 'o', 'a', 'l', 'a'], ['r', 'a', 'p', 'o', 's', 'a'], ['i', 'g', 'u', 'a', 'n', 'a']]
comida = [['p', 'i', 'p', 'o', 'c', 'a'], ['c', 'a', 'v', 'i', 'a', 'r'], ['m', 'o', 's', 't', 'a', 'r', 'd', 'a']]
pais = [['c', 'a', 'n', 'a', 'd', 'á'], ['h', 'u', 'n', 'g', 'r', 'i', 'a'], ['b', 'a', 'h', 'a', 'm', 'a', 's']]

# TODO: enviar apenas os dados de montagem do boneco, o cliente é
#       quem pega a estrutura e desenha localmente.
# TODO: pensar num jeito de limitar o argumento para 1 - 6
def desenhaBoneco(chances):
    # TODO: talvez sejam números hardcodeds, refatorar essa seção?!
    membrosIndices = [50, 67, 66, 68, 84, 86]
    cabeca = 50
    torax = 67
    bracoEsq = 66
    bracoDir = 68
    pernaEsq = 84
    pernaDir = 86

    bonecoStr = """
        --------
        |      |
        |      O
        |     /|\\
        |     / \\
        |      
        --------
        """

    boneco = list(bonecoStr)
    bonecoCompleto = boneco

    # sumindo com os membros, a variável 'bonecoStr' serve
    # apenas como visualização do corpo completo
    for i in membrosIndices:
        boneco[i] = " "

    # que falta faz um switch case
    if chances == 6:
        return boneco

    elif chances == 5:
        boneco[cabeca] = "O"
        return boneco

    elif chances == 4:
        boneco[cabeca] = "O"
        boneco[torax] = "|"
        return boneco

    elif chances == 3:
       boneco[cabeca] = "O"
       boneco[torax] = "|"
       boneco[bracoEsq] = "/"
       return boneco

    elif chances == 2:
       boneco[cabeca] = "O"
       boneco[torax] = "|"
       boneco[bracoEsq] = "/"
       boneco[bracoDir] = "\\"
       return boneco

    elif chances == 1:
       boneco[cabeca] = "O"
       boneco[torax] = "|"
       boneco[bracoEsq] = "/"
       boneco[bracoDir] = "\\"
       boneco[pernaEsq] = "/"
       return boneco

    return bonecoCompleto

def caixinha(texto):
    linhas = texto.strip().split('\n')
    print("---------------------")
    for linha in linhas:
        print(f"| {linha:<18} |")
    print("---------------------")

# Iniciar socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((SERVER_IP, SERVER_PORTA))
servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_tcp.bind((SERVER_IP, SERVER_PORTA - 1))
servidor_tcp.listen(1)
conn, addr = servidor_tcp.accept()
grupos = " ".join("Escolha um tema: \n[1] Animal \n[2]Comida \n[3]País")

print("Aguardando quem ousa me desafiar...")

while True:
    conn.send(f"Escolha um grupo de palavras \n{grupos}: ".encode())
    grupo = conn.recv(1024).decode()
    # Espera o cliente enviar "iniciar"
    data, address = servidor.recvfrom(1024)

    usuarioEscolheu = int(grupo)
    if usuarioEscolheu == 1:
        palavraRodada = random.choice(animal)
    elif usuarioEscolheu == 2:
        palavraRodada = random.choice(comida)
    else:
        palavraRodada = random.choice(pais)

    letrasChutadas = []
    letrasAcertadas = []
    chances = 6
    under = ""
    for i in palavraRodada:
        under += "* "

    mensagemInicial = f"{under}\n\n{desenhaBoneco(chances)}"
    caixinha(mensagemInicial)
    servidor.sendto(mensagemInicial.encode(), address)
    
    while True:
        letraData, _ = servidor.recvfrom(1024)
        letra = letraData.decode().strip().lower()

        if letra not in palavraRodada:
            chances -= 1
            mostrarLetra = ""
            for i in palavraRodada:
                if i in letrasAcertadas:
                    mostrarLetra += i + " "
            mensagem = f"Errou! Chances: {chances}\n{mostrarLetra}\n\n{desenhaBoneco(chances)}"
            caixinha(mensagem)
            servidor.sendto(mensagem.encode(), address)
        else:
            letrasAcertadas.append(letra)
            mostrarLetra = ""
            certos = 0
            for i in palavraRodada:
                if i in letrasAcertadas:
                    mostrarLetra += i + " "
                    certos += 1
            if certos == len(palavraRodada):
                break
            mensagem = f"Acertou!\n{mostrarLetra}\n\n{desenhaBoneco(chances)}"
            caixinha(mensagem)
            servidor.sendto(mensagem.encode(), address)
        

        if letra in letrasChutadas:
            mensagem = f"Letra repetida, tente outra!\n\n{desenhaBoneco(chances)}"
            caixinha(mensagem)
            servidor.sendto(mensagem.encode(), address)
            continue

        letrasChutadas.append(letra)

        if chances == 0:
            mensagem = f"Game Over! A palavra era: {''.join(palavraRodada)}\n\n{desenhaBoneco(chances)}"
            caixinha(mensagem)
            servidor.sendto(mensagem.encode(), address)
            servidor.close()
            break
        if len(palavraRodada) == len(letrasAcertadas):
            break
    
    if (chances != 0):
        mensagem = f"Deu certo, você acertou e ganhou!\nPalavra: {''.join(palavraRodada)}\n\n{desenhaBoneco(chances)}"
        caixinha(mensagem)
        servidor.sendto(mensagem.encode(), address)
        servidor.close()

