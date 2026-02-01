# Copilot Instructions - Projeto de Segurança de Rede

## Overview

Este projeto é um **sistema de monitorização e auditoria de redes locais** em Python. Implementa três componentes principais que trabalham juntos para escanear dispositivos, armazenar dados e gerar relatórios de segurança.

## Architecture & Data Flow

```
scanner_rede.py
├─ escaneador_rede() → ARP scanning via Scapy
├─ salvar_no_db() → persiste em SQLite
└─ buscar_fabricante() → consulta API externa (macvendors.com)

↓ SQLite DB (seguranca_redes.db)
├─ Tabela: dispositivos
│  └─ Campos: ip, mac (PRIMARY KEY), fabricante, ultima_vez_visto
│
gerar_relatorio.py → Lê DB, gera relatorio_seguranca_DD-MM-YYYY.txt
consultar_banco.py → Consulta interativa do DB
```

**Key Pattern**: BD-driven architecture com base de dados como fonte de verdade central. Todos os scripts dependem de `seguranca_redes.db` no diretório do projeto.

## Project-Specific Conventions

### Path Management
- **Critical**: Use `os.path.dirname(os.path.abspath(__file__))` para obter BASE_DIR
- Construa caminhos com `os.path.join(BASE_DIR, filename)` para garantir compatibilidade
- Exemplo em [scanner_rede.py](scanner_rede.py#L12-L13) e [gerar_relatorio.py](gerar_relatorio.py#L5-L6)

### Database Operations
- DB inicialização via `iniciar_db()` (verifica CREATE TABLE IF NOT EXISTS)
- Use **INSERT OR REPLACE** para atualizar timestamps de dispositivos (idempotente)
- Sempre feche conexões com `conn.close()` após operações

### External API Integration
- **macvendors.com API**: usado para identificar fabricantes por MAC address
- Timeout: 3 segundos; fallback para "Desconhecido" ou "Erro na consulta"
- Sem autenticação requerida, mas rate-limit implícito

### Network Scanning
- **Target format**: CIDR notation (ex: "192.168.0.1/24")
- Usa Scapy ARP scan com broadcast ethernet
- Windows: usa `ping -n 1 {broadcast}` para "acordar" dispositivos antes do scan

### Report Generation
- **Date format**: DD-MM-YYYY (em timestamps e nomes de arquivo)
- Encoding: UTF-8 obrigatório
- Alertas automáticos baseados em padrões de fabricante (TERACOM, CLOUD NETWORK)
- [gerar_relatorio.py](gerar_relatorio.py#L33-L42) contém lógica de detecção de risco simples

## Dependencies & External Services

- **sqlite3**: built-in
- **scapy**: ARP scanning (requer instalação)
- **requests**: consultas HTTP a macvendors.com (requer instalação)

## Common Workflows

### 1. Escanear Rede
```bash
python scanner_rede.py
```
- Ajuste `alvo = "192.168.0.1/24"` conforme sua rede

### 2. Gerar Relatório
```bash
python gerar_relatorio.py
```
- Cria arquivo `relatorio_seguranca_DD-MM-YYYY.txt`

### 3. Consultar BD
```bash
python consultar_banco.py
```
- Lista dispositivos em ordem decrescente de último avistamento

## Enhancement Points for AI Agents

When adding features, consider:

1. **DB Schema Extensions**: Adicione colunas via ALTER TABLE (não DROP)
2. **New Detection Rules**: Estenda a lógica de alerta em [gerar_relatorio.py](gerar_relatorio.py#L33-L42)
3. **Report Formats**: Mantenha compatibilidade com timestamp `YYYY-MM-DD HH:MM:SS` em registros
4. **Error Handling**: APIs podem falhar silenciosamente; sempre forneça fallbacks
5. **Path Portability**: Use `os.path.join()` em todos os caminhos de arquivo

---
*Last updated: 2026-02-01*
