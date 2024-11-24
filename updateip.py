import os

def find_server_properties_files(base_directory):
    server_files = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file == "server.properties":
                server_files.append(os.path.join(root, file))
    return server_files

def update_server_ip(file_paths):
    ip_address = "0.0.0.0"  # Definir o IP fixo para 0.0.0.0

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Atualiza a linha `server-ip=` com o IP fixo
        with open(file_path, 'w') as file:
            for line in lines:
                if line.startswith("server-ip="):
                    file.write(f"server-ip={ip_address}\n")
                else:
                    file.write(line)

        print(f"Endereço IP atualizado com sucesso no arquivo {file_path}!")

if __name__ == "__main__":
    # Caminho do diretório base onde estão localizados os arquivos `server.properties`
    base_directory = 'caminho da sua pasta de servidores'  # Modifique para o caminho desejado

    # Encontra todos os arquivos `server.properties` na estrutura de diretórios
    files = find_server_properties_files(base_directory)

    # Atualiza o IP em cada arquivo encontrado
    update_server_ip(files)
