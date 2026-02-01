import sqlite3

def consultar_dispositivos():
    conn = sqlite3.connect('seguranca_redes.db')
    cursor = conn.cursor()
    
    # SQL para selecionar tudo da tabela
    cursor.execute("SELECT * FROM dispositivos ORDER BY ultima_vez_visto DESC")
    
    colunas = [description[0] for description in cursor.description]
    print(f"{colunas[0]:<15} | {colunas[1]:<18} | {colunas[2]:<30} | {colunas[3]}")
    print("-" * 85)
    
    for linha in cursor.fetchall():
        print(f"{linha[0]:<15} | {linha[1]:<18} | {linha[2]:<30} | {linha[3]}")
    
    conn.close()

if __name__ == "__main__":
    consultar_dispositivos()