import os
import random
import string
import json
import time
import logging

# Configura o log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_database_path(base_directory):
    """Retorna o caminho completo do banco de dados no mesmo diretório onde o script está escaneando."""
    return os.path.join(base_directory, "ports_database.json")

def load_database(base_directory):
    """Carrega o banco de dados do arquivo JSON."""
    database_path = get_database_path(base_directory)
    if os.path.exists(database_path):
        try:
            with open(database_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            logging.warning(f"Arquivo {database_path} está corrompido. Recriando banco de dados.")
            return {}
    return {}

def save_database(base_directory, database):
    """Salva o banco de dados no arquivo JSON no diretório base."""
    database_path = get_database_path(base_directory)
    try:
        with open(database_path, 'w') as file:
            json.dump(database, file, indent=4)
        logging.info(f"Banco de dados salvo em {database_path}")
    except Exception as e:
        logging.error(f"Erro ao salvar o banco de dados: {e}")

def generate_random_port(range_start, range_end, exclude_ports):
    """Gera uma porta aleatória dentro de um intervalo, excluindo portas específicas e já utilizadas."""
    attempts = 0
    while attempts < 1000:  # Evitar loop infinito
        port = random.randint(range_start, range_end)
        if port not in exclude_ports:
            return port
        attempts += 1
    raise ValueError("Não foi possível gerar uma porta aleatória não utilizada.")

def generate_random_password(length=16):
    """Gera uma senha aleatória com letras, números e caracteres especiais."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def is_bedrock_server(server_directory):
    """Verifica se o servidor é do tipo Bedrock (contém o arquivo bedrock_server.exe)."""
    return os.path.exists(os.path.join(server_directory, 'bedrock_server.exe'))

def find_server_properties_files(base_directory):
    """Encontra todos os arquivos server.properties dentro do diretório base e seus subdiretórios."""
    file_paths = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file == "server.properties":
                file_paths.append(os.path.join(root, file))
    return file_paths

def remove_deleted_servers_from_database(database, file_paths, base_directory):
    """
    Remove servidores do banco de dados que não têm mais um diretório associado.
    """
    active_server_ids = {os.path.basename(os.path.dirname(file_path)) for file_path in file_paths}
    all_server_ids = set(database.keys())
    deleted_servers = all_server_ids - active_server_ids

    for server_id in deleted_servers:
        logging.info(f"Removendo servidor ausente do banco de dados: {server_id}")
        del database[server_id]

    if deleted_servers:
        save_database(base_directory, database)

def update_server_properties(file_paths, database, base_directory):
    """Atualiza os arquivos `server.properties` com base no banco de dados e configurações."""
    used_ports = [entry["server_port"] for entry in database.values() if entry["server_port"]]
    used_ports += [entry["server-portv6"] for entry in database.values() if entry["server-portv6"]]

    for file_path in file_paths:
        server_directory = os.path.dirname(file_path)

        # Verifica se o diretório do servidor existe
        if not os.path.exists(server_directory):
            logging.info(f"Pasta do servidor {server_directory} foi apagada. Removendo do banco de dados.")
            server_id = os.path.basename(server_directory)
            if server_id in database:
                del database[server_id]
            continue  # Pula o processamento deste servidor

        is_bedrock = is_bedrock_server(server_directory)
        server_id = os.path.basename(server_directory)

        # Adiciona ao banco de dados se não existir
        if server_id not in database:
            database[server_id] = {
                "rcon_password": None,
                "rcon_port": None,
                "server_port": None,
                "server-portv6": None,
                "is_bedrock": is_bedrock
            }

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            logging.error(f"Erro ao ler o arquivo {file_path}: {e}")
            continue

        updated_lines = []
        for line in lines:
            key, value = (line.split('=')[0].strip(), line.split('=')[1].strip()) if '=' in line else (None, None)

            if key == "server-port":
                if database[server_id]["server_port"] is None:
                    new_port = generate_random_port(1024, 32254, used_ports)
                    database[server_id]["server_port"] = new_port
                    used_ports.append(new_port)
                    updated_lines.append(f"server-port={new_port}\n")
                    logging.info(f"Porta para {server_id} configurada como {new_port}")
                else:
                    updated_lines.append(f"server-port={database[server_id]['server_port']}\n")
            elif key == "server-portv6" and is_bedrock:
                if database[server_id]["server-portv6"] is None:
                    new_portv6 = generate_random_port(1024, 32254, used_ports)
                    database[server_id]["server-portv6"] = new_portv6
                    used_ports.append(new_portv6)
                    updated_lines.append(f"server-portv6={new_portv6}\n")
                    logging.info(f"Porta v6 para {server_id} configurada como {new_portv6}")
                else:
                    updated_lines.append(f"server-portv6={database[server_id]['server-portv6']}\n")
            elif key == "rcon.port" and not is_bedrock:
                if database[server_id]["rcon_port"] is None:
                    new_rcon_port = generate_random_port(32255, 65535, used_ports)
                    database[server_id]["rcon_port"] = new_rcon_port
                    used_ports.append(new_rcon_port)
                    updated_lines.append(f"rcon.port={new_rcon_port}\n")
                    logging.info(f"Porta RCON para {server_id} configurada como {new_rcon_port}")
                else:
                    updated_lines.append(f"rcon.port={database[server_id]['rcon_port']}\n")
            elif key == "rcon.password":
                if database[server_id]["rcon_password"] is None:
                    new_password = generate_random_password()
                    database[server_id]["rcon_password"] = new_password
                    updated_lines.append(f"rcon.password={new_password}\n")
                else:
                    updated_lines.append(f"rcon.password={database[server_id]['rcon_password']}\n")
            else:
                updated_lines.append(line)

        try:
            with open(file_path, 'w') as file:
                file.writelines(updated_lines)
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo {file_path}: {e}")
            continue

        save_database(base_directory, database)

# Caminho base onde estão os servidores
base_directory = "caminho da sua pasta de servid"

# Carrega o banco de dados ou cria um novo
database = load_database(base_directory)

# Encontra todos os arquivos server.properties
file_paths = find_server_properties_files(base_directory)

# Executa continuamente
while True:
    remove_deleted_servers_from_database(database, file_paths, base_directory)
    update_server_properties(file_paths, database, base_directory)
    logging.info("Aguardando 10 segundos para a próxima atualização...")
    time.sleep(10)