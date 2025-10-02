import pandas as pd
import numpy as np
import datetime

def gerar_dados_vendas():
    """Gera um DataFrame com dados de vendas históricos e salva em um CSV."""
    print("Iniciando a geração de dados de vendas...")
    
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2025, 9, 30)
    date_range = pd.date_range(start_date, end_date)

    produtos = {
        "PROD001": {"nome": "Notebook Gamer", "base_vendas": 10, "tendencia": 0.05},
        "PROD002": {"nome": "Mouse Sem Fio", "base_vendas": 50, "tendencia": 0.01},
        "PROD003": {"nome": "Teclado Mecanico", "base_vendas": 30, "tendencia": 0.02},
        "PROD004": {"nome": "Monitor 4K", "base_vendas": 15, "tendencia": 0.03}
    }

    data_list = []

    for single_date in date_range:
        for prod_id, prod_info in produtos.items():
            day_of_week_factor = 1.2 if single_date.weekday() < 5 else 0.8
            dias_passados = (single_date.date() - start_date).days
            tendencia_factor = 1 + (prod_info["tendencia"] * (dias_passados / 30))
            seasonal_factor = 1.5 if single_date.month in [11, 12] else 1.0
            vendas = int(prod_info["base_vendas"] * day_of_week_factor * tendencia_factor * seasonal_factor * (1 + np.random.rand() * 0.2))
            data_list.append([single_date, prod_id, prod_info["nome"], vendas])

    df = pd.DataFrame(data_list, columns=["data_da_venda", "id_produto", "nome_produto", "quantidade_vendida"])
    
    df.to_csv('vendas_historicas.csv', index=False)
    
    print("Arquivo 'vendas_historicas.csv' criado com sucesso!")
    print(f"Total de registros: {len(df)}")
    print("Amostra dos dados:")
    print(df.head())

if __name__ == '__main__':
    gerar_dados_vendas()