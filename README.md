# script para alocar portas no minecraft tanto server port e rcon e senha rcon

Explicação do Funcionamento do Script
Este script é projetado para automatizar a configuração e a atualização de arquivos server.properties de servidores Minecraft, tanto para a versão Java quanto para a Bedrock, gerenciando portas e senhas de maneira eficiente. Ele também mantém um banco de dados (no formato JSON) para garantir que as configurações sejam persistidas e gerenciadas adequadamente.

Como o Script Funciona
Carregamento do Banco de Dados: O script começa carregando um banco de dados JSON existente, que contém informações sobre os servidores, como as portas usadas, a senha RCON e se o servidor é do tipo Bedrock. Se o banco de dados não existir ou estiver corrompido, ele cria um novo banco vazio.

Localização dos Arquivos server.properties: O script busca por arquivos server.properties dentro do diretório de servidores fornecido (base_directory). Ele percorre recursivamente as pastas e armazena os caminhos desses arquivos para depois atualizar suas configurações.

Verificação do Tipo de Servidor (Bedrock ou Java): O script verifica se o servidor é do tipo Bedrock (presença do arquivo bedrock_server.exe), o que é importante para determinar quais portas e configurações aplicar.

Geração de Portas e Senhas:

O script gera portas aleatórias dentro de um intervalo predefinido, garantindo que as portas não sejam duplicadas para outros servidores (usando o banco de dados para rastrear as portas já utilizadas).
Para servidores Java, ele também gera uma porta RCON aleatória se necessário.
Caso o servidor não tenha uma senha RCON definida, o script gera uma senha aleatória e a atribui ao arquivo server.properties.
Remoção de Servidores Inativos: O script verifica periodicamente se algum servidor foi apagado, removendo-os do banco de dados caso o diretório correspondente não exista mais.

Atualização dos Arquivos server.properties: Para cada arquivo server.properties, o script atualiza os campos de porta e senha RCON (se necessário), garantindo que cada servidor tenha configurações exclusivas. Ele então salva novamente o arquivo server.properties com as novas configurações.

Persistência das Configurações: Após cada execução, o banco de dados é salvo para garantir que as alterações nas configurações (como portas atribuídas) sejam armazenadas e possam ser reutilizadas nas próximas execuções.

Execução Contínua: O script entra em um loop infinito, realizando atualizações a cada 10 segundos. Isso permite que ele esteja sempre monitorando os servidores e realizando as atualizações necessárias de maneira contínua.

Como Usar o Script
Configuração Inicial:

Coloque o script em um diretório onde você tenha acesso de leitura e gravação.
Defina o caminho do diretório de servidores no parâmetro base_directory, substituindo o valor do caminho no código (/home/usuario/servers).
Instalação do Python:

Certifique-se de ter o Python 3.x instalado em sua máquina. O script usa apenas bibliotecas padrão, então não é necessário instalar dependências extras.
Verifique se o Python está configurado corretamente no seu sistema com o comando:
python --version

Conclusão
Este script é uma solução automatizada para gerenciar múltiplos servidores Minecraft, economizando tempo e garantindo que as configurações de portas, senhas e outros parâmetros sejam sempre únicas e corretas,
Este script é uma solução automatizada para gerenciar múltiplos servidores Minecraft, economizando tempo e garantindo que as configurações de portas, senhas e outros parâmetros sejam sempre únicas e corretas. 
