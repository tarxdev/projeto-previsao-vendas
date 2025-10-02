import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score

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

    df_teste = df_com_features[df_com_features['data_da_venda'] >= '2025-08-01']

    features = ['ano', 'mes', 'dia', 'dia_da_semana', 'id_produto_num']
    alvo = 'quantidade_vendida'

    X_teste = df_teste[features]
    y_teste = df_teste[alvo]

    print("Carregando o modelo salvo...")
    modelo = joblib.load('modelo_vendas.pkl')

    print("Realizando previsões no conjunto de teste...")
    previsoes = modelo.predict(X_teste)

    mae = mean_absolute_error(y_teste, previsoes)
    r2 = r2_score(y_teste, previsoes)

    print("\n--- Resultados da Avaliação ---")
    print(f"MAE (Erro Absoluto Médio): {mae:.2f}")
    print(f"R² (Coeficiente de Determinação): {r2:.2f}")

    print("\nExplicação dos resultados:")
    print(f"-> MAE: Em média, as previsões do modelo erram em aproximadamente {mae:.0f} unidades de venda (para mais ou para menos).")
    print(f"-> R²: O modelo consegue explicar aproximadamente {r2:.1%} da variação nas vendas.")

    df_resultados = pd.DataFrame({'Real': y_teste, 'Previsão': previsoes})
    print("\n--- Amostra de Previsões vs. Valores Reais ---")
    print(df_resultados.head(10))