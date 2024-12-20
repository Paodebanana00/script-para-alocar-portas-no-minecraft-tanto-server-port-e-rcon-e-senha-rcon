import collections
import struct
import socket

bufsize = 4096

Packet = collections.namedtuple("Packet", ("ident", "kind", "payload"))

class IncompletePacket(Exception):
    def __init__(self, minimum):
        self.minimum = minimum

def decode_packet(data):
    if len(data) < 14:
        raise IncompletePacket(14)

    length = struct.unpack("<i", data[:4])[0] + 4
    if len(data) < length:
        raise IncompletePacket(length)

    ident, kind = struct.unpack("<ii", data[4:12])
    payload, padding = data[12:length-2], data[length-2:length]
    assert padding == b"\x00\x00"
    return Packet(ident, kind, payload), data[length:]

def encode_packet(packet):
    data = struct.pack("<ii", packet.ident, packet.kind) + packet.payload + b"\x00\x00"
    return struct.pack("<i", len(data)) + data

def receive_packet(sock):
    data = b""
    while True:
        try:
            return decode_packet(data)[0]
        except IncompletePacket as exc:
            while len(data) < exc.minimum:
                data += sock.recv(exc.minimum - len(data))

def send_packet(sock, packet):
    sock.sendall(encode_packet(packet))

def login(sock, password):
    send_packet(sock, Packet(0, 3, password.encode("utf8")))
    packet = receive_packet(sock)
    return packet.ident == 0

def command(sock, text):
    send_packet(sock, Packet(0, 2, text.encode("utf8")))
    send_packet(sock, Packet(1, 0, b""))
    response = b""
    while True:
        packet = receive_packet(sock)
        if packet.ident != 0:
            break
        response += packet.payload
    return response.decode("utf8")

def create_socket(host, port):
    """Cria um socket e tenta conectar ao host e porta fornecidos usando IPv4 ou IPv6"""
    print(f"Tentando conectar ao servidor: {host} na porta {port}")
    sock = None
    for family in [socket.AF_INET6, socket.AF_INET]:  # Tenta primeiro IPv6 e depois IPv4
        try:
            sock = socket.socket(family, socket.SOCK_STREAM)
            sock.settimeout(10)  # Definir tempo limite de conexão
            sock.connect((host, port))
            print(f"Conectado com sucesso a {host}:{port} usando {'IPv6' if family == socket.AF_INET6 else 'IPv4'}")
            break
        except socket.gaierror as e:
            print(f"Erro ao resolver o endereço (família {family}): {e}")
        except socket.error as e:
            print(f"Erro de conexão (família {family}): {e}")
            if sock:
                sock.close()
    if not sock:
        raise Exception("Falha ao conectar usando IPv4 ou IPv6.")
    return sock

# Função principal
def main():
    # Nome de domínio (pode ser qualquer domínio com um registro AAAA ou A válido) ou ipv4 e 6
    RCON_HOST = "seu domínio ou ip"  # Substitua pelo nome do seu servidor
    RCON_PORT = 25575  # Porta RCON (padrão é 25575)
    RCON_PASSWORD = "euvimpradaprati"  # Substitua pela senha configurada

    sock = None
    try:
        # Cria o socket e tenta conectar usando IPv6 ou IPv4 automaticamente
        sock = create_socket(RCON_HOST, RCON_PORT)
        print(f"Conectado ao servidor RCON em {RCON_HOST}:{RCON_PORT}")
        
        # Faz login
        if login(sock, RCON_PASSWORD):
            print("Login bem-sucedido!")
        
        while True:
            # Solicita um comando
            command_input = input("Digite o comando para o servidor (ou 'sair' para sair): ")
            if command_input.lower() == "sair":
                print("Saindo...")
                break
            
            # Envia o comando e mostra a resposta
            response = command(sock, command_input)
            print("Resposta do servidor:", response)
    
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if sock:
            sock.close()

if __name__ == "__main__":
    main()
