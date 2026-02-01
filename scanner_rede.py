import sqlite3
import requests
from scapy.all import ARP, Ether, srp
from datetime import datetime
import os

def acordar_dispositivos(ip_range):
    # Um ping rápido para o broadcast da rede pode forçar o celular a responder
    # No Windows é -n 1, no Linux é -c 1
    base_ip = ".".join(ip_range.split(".")[:-1])
    print(f"[*] Tentando 'acordar' dispositivos no range {base_ip}.x ...")
    # Tenta pingar o endereço de broadcast (geralmente .255)
    os.system(f"ping -n 1 {base_ip}.255 > nul")

# Pega o caminho da pasta onde o script .py está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "seguranca_redes.db")

def iniciar_db():
    # Agora usamos o DB_PATH que garante o local correto
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dispositivos 
                 (ip TEXT, mac TEXT PRIMARY KEY, fabricante TEXT, ultima_vez_visto DATETIME)''')
    conn.commit()
    conn.close()
    print(f"[*] Banco de dados verificado em: {DB_PATH}")

def salvar_no_db(dispositivos):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for d in dispositivos:
        # Usamos INSERT OR REPLACE para atualizar a "última vez visto" se o MAC já existir
        c.execute('''INSERT OR REPLACE INTO dispositivos (ip, mac, fabricante, ultima_vez_visto) 
                     VALUES (?, ?, ?, ?)''', (d['ip'], d['mac'], d['fabricante'], datetime.now()))
    conn.commit()
    conn.close()

# --- LÓGICA DE REDE ---
def buscar_fabricante(mac):
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=3)
        return response.text if response.status_code == 200 else "Desconhecido"
    except:
        return "Erro na consulta"

def escaneador_rede(ip_range):
    print(f"[*] Escaneando a rede {ip_range}...")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    resultado = srp(ether/arp, timeout=2, verbose=False)[0]

    lista_dispositivos = []
    for _, recebido in resultado:
        mac = recebido.hwsrc
        lista_dispositivos.append({
            'ip': recebido.psrc,
            'mac': mac,
            'fabricante': buscar_fabricante(mac)
        })
    return lista_dispositivos

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    iniciar_db()
    
    # Alvo: sua rede local (ajuste se necessário)
    alvo = "192.168.0.1/24" 
    
    encontrados = escaneador_rede(alvo)
    salvar_no_db(encontrados)
    
    print("\n" + "="*70)
    print(f"{'IP':<15} | {'MAC Address':<18} | {'Fabricante'}")
    print("="*70)
    for d in encontrados:
        print(f"{d['ip']:15} | {d['mac']:18} | {d['fabricante']}")
    print("="*70)
    print(f"\n[!] Sucesso: {len(encontrados)} dispositivos salvos no banco de dados.")