import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def criar_features(df):
    df['data_da_venda'] = pd.to_datetime(df['data_da_venda'])
    df['ano'] = df['data_da_venda'].dt.year
    df['mes'] = df['data_da_venda'].dt.month
    df['dia'] = df['data_da_venda'].dt.day
    df['dia_da_semana'] = df['data_da_venda'].dt.dayofweek
    return df

if __name__ == '__main__':
    df = pd.read_csv('vendas_historicas.csv')
    df_com_features = criar_features(df)
    
    df_com_features['id_produto_num'] = df_com_features['id_produto'].astype('category').cat.codes
    
    print("Dados preparados com features e encoding:")
    print(df_com_features.head())
    
    df_treino = df_com_features[df_com_features['data_da_venda'] < '2025-08-01']
    df_teste = df_com_features[df_com_features['data_da_venda'] >= '2025-08-01']
    
    print(f"\nTamanho do conjunto de treino: {len(df_treino)} registros")
    print(f"Tamanho do conjunto de teste: {len(df_teste)} registros")
    
    features = ['ano', 'mes', 'dia', 'dia_da_semana', 'id_produto_num']
    alvo = 'quantidade_vendida'
    
    X_treino = df_treino[features]
    y_treino = df_treino[alvo]
    X_teste = df_teste[features]
    y_teste = df_teste[alvo]
    
    print("\nIniciando o treinamento do modelo RandomForestRegressor...")
    
    modelo = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=5)
    
    modelo.fit(X_treino, y_treino)
    
    print("\nModelo treinado com sucesso!")

import joblib

joblib.dump(modelo, 'modelo_vendas.pkl')

print("Modelo salvo em 'modelo_vendas.pkl'")