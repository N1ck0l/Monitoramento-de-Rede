🛡️ Network Asset Monitor (NAM) - Python & Scapy
O Network Asset Monitor é uma ferramenta de reconhecimento de rede e inventário de ativos desenvolvida para automação de segurança cibernética. O sistema realiza varreduras em camada 2 (ARP), identifica fabricantes de dispositivos via API de OUI e armazena o histórico em um banco de dados local para auditoria e detecção de anomalias.

🚀 Funcionalidades
Varredura ARP: Identificação de dispositivos ativos na rede local ignorando bloqueios de Firewall (ICMP).

Vendor Identification: Consulta automática de fabricantes de placas de rede para identificação de hardware (Ex: Sony, Panasonic, Teracom).

Persistência de Dados: Armazenamento em SQLite com atualização automática da "última vez visto".

Relatório de Auditoria: Geração de relatórios em texto com análise básica de risco e política de ativos.

Detecção de Disponibilidade: Lógica para identificar dispositivos que "sumiram" da rede.

🛠️ Tecnologias Utilizadas
Python 3.11+

Scapy: Manipulação e envio de pacotes de rede.

SQLite: Banco de dados relacional leve para inventário.

Requests: Integração com APIs externas de Mac Vendors.

OS/DateTime: Manipulação de caminhos de arquivos e logs temporais.

📋 Pré-requisitos
Para rodar este projeto, você precisará ter o Python instalado e privilégios de administrador (necessário para o Scapy interagir com a interface de rede).

Bash
# Instalação das dependências
pip install scapy requests
🖥️ Como Usar
Clone este repositório.

Abra o terminal como Administrador.

Execute o script principal:

Bash
python scanner_rede.py
Consulte o banco de dados gerado ou o relatório TXT na pasta do projeto.

📝 Próximos Passos (Roadmap)
[ ] Implementar interface gráfica com Streamlit.

[ ] Criar sistema de notificações via Telegram Bot.

[ ] Adicionar funcionalidade de "Lista Branca" (Dispositivos Autorizados).

[ ] Dockerizar a aplicação para execução em servidores de rede.
