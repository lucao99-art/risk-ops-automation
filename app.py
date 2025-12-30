import pandas as pd
import sqlite3 
from datetime import datetime 

class GestorProdutividade: 
    def __init__(self, db_name='operacao_risco.db'):
        self.conn = sqlite3.connect(db_name)
        self.criar_tabela()

    def criar_tabela(self): 
        cursor = self.conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS produtividade ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                analista TEXT NOT NULL, 
                chats_atendidos INTEGER NOT NULL, 
                data_registro TEXT NOT NULL
            ) 
        ''') 
        self.conn.commit()

    def salvar_dados(self, analista, qtd_chats):
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO produtividade (analista, chats_atendidos, data_registro)
            VALUES (?, ?, ?)
        ''', (analista, qtd_chats, data_atual))
        self.conn.commit() 
        print(f"\n✅ Dados de {analista} salvos no banco SQLite!")   

    def gerar_dashboard(self): 
        df = pd.read_sql_query("SELECT * FROM produtividade", self.conn) 
        
        if df.empty: 
            print("\n⚠️ Nenhum dado registrado ainda.")
            return 
        
        df['Chats_por_Hora'] = (df['chats_atendidos'] / 12).round(2) 

        print("\n--- 📊 DASHBOARD DE PRODUTIVIDADE N1 ---") 
        print(df[['analista', 'chats_atendidos', 'Chats_por_Hora', 'data_registro']]) 

        # Salva o CSV para você enviar à supervisão
        df.to_csv('relatorio_n1.csv', index=False) 
        print("\n💾 Relatório 'relatorio_n1.csv' gerado com sucesso!")

# --- O código abaixo deve estar fora da classe (sem espaços no início da linha) ---
gestor = GestorProdutividade() 

while True: 
    print("\n[1] Registrar Produção N1")
    print("[2] Ver Dashboard e Gerar CSV")
    print("[3] Sair")

    escolha = input("Selecione uma opção: ")

    if escolha == '1':
        nome = input("Nome do Analista: ")
        chats = int(input("Total de Chats no turno: "))
        gestor.salvar_dados(nome, chats)
    elif escolha == '2': 
        gestor.gerar_dashboard() 
    elif escolha == '3':
        print("Encerrando... Bom trabalho para quem fica!")
        break