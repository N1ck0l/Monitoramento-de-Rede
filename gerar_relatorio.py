import sqlite3
import os
from datetime import datetime

def gerar_relatorio_txt():
    # Caminho do banco (ajustado conforme sua configuração anterior)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "seguranca_redes.db")
    relatorio_path = os.path.join(base_dir, f"relatorio_seguranca_{datetime.now().strftime('%d-%m-%Y')}.txt")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dispositivos")
    dispositivos = cursor.fetchall()
    conn.close()

    with open(relatorio_path, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("      RELATÓRIO DE AUDITORIA DE REDE - NICKOLAS SEGURANÇA\n")
        f.write(f"      Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")

        f.write(f"SUMÁRIO EXECUTIVO:\n")
        f.write(f"- Total de dispositivos mapeados: {len(dispositivos)}\n")
        f.write(f"- Estado da Rede: MONITORADA\n\n")

        f.write("DETALHAMENTO DOS ATIVOS:\n")
        f.write(f"{'IP':<15} | {'MAC Address':<18} | {'Fabricante'}\n")
        f.write("-" * 60 + "\n")

        for ip, mac, fab, visto in dispositivos:
            f.write(f"{ip:<15} | {mac:<18} | {fab}\n")
            
        f.write("\n" + "="*60 + "\n")
        f.write("ANÁLISE DE RISCO PRELIMINAR:\n")
        
        # Lógica simples de alerta
        for ip, mac, fab, visto in dispositivos:
            if "TERACOM" in fab.upper():
                f.write(f"[!] INFO: Gateway detectado ({fab}). Verificar firmware.\n")
            if "CLOUD NETWORK" in fab.upper():
                f.write(f"[!] ALERTA: Dispositivo móvel/notebook detectado. Verificar política de BYOD.\n")
        
        f.write("\nFim do Relatório. Gerado automaticamente pelo Sistema de Monitorização.\n")

    print(f"[*] Relatório gerado com sucesso: {relatorio_path}")

if __name__ == "__main__":
    gerar_relatorio_txt()