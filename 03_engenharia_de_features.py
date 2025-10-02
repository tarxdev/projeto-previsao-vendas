import pandas as pd

def criar_features(df):
    """Cria features de data a partir da coluna 'data_da_venda'."""
    df['data_da_venda'] = pd.to_datetime(df['data_da_venda'])
    df['ano'] = df['data_da_venda'].dt.year
    df['mes'] = df['data_da_venda'].dt.month
    df['dia'] = df['data_da_venda'].dt.day
    df['dia_da_semana'] = df['data_da_venda'].dt.dayofweek 
    print("Novas colunas de data criadas com sucesso!")
    return df

if __name__ == '__main__':
    df = pd.read_csv('vendas_historicas.csv')
    
    df_com_features = criar_features(df)
    
    print("\nAmostra dos dados com as novas features:")
    print(df_com_features.head())
    
    print("\nNovas informações do DataFrame:")
    df_com_features.info()