import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_dados():
    """Carrega os dados de vendas e gera visualizações exploratórias."""
    print("Iniciando a análise exploratória dos dados...")
    
    # Carrega o arquivo CSV gerado anteriormente
    df = pd.read_csv('vendas_historicas.csv')
    
    # --- 1. Preparação dos Dados ---
    # Converte a coluna de data para o tipo datetime, que é essencial para séries temporais
    df['data_da_venda'] = pd.to_datetime(df['data_da_venda'])
    print("\nTipos de dados após conversão:")
    df.info()
    
    # --- 2. Análise Descritiva ---
    print("\nResumo estatístico da quantidade vendida:")
    print(df['quantidade_vendida'].describe())
    
    # --- 3. Visualizações ---
    
    # Gráfico 1: Vendas totais ao longo do tempo
    print("\nGerando gráfico de vendas totais ao longo do tempo...")
    vendas_por_dia = df.groupby('data_da_venda')['quantidade_vendida'].sum()
    
    plt.figure(figsize=(15, 6))
    plt.plot(vendas_por_dia.index, vendas_por_dia.values, label='Vendas Totais Diárias')
    plt.title('Vendas Totais Diárias (2024-2025)')
    plt.xlabel('Data')
    plt.ylabel('Quantidade Vendida')
    plt.grid(True)
    plt.legend()
    plt.show() # Exibe o gráfico
    
    # Gráfico 2: Total de vendas por produto
    print("Gerando gráfico de total de vendas por produto...")
    vendas_por_produto = df.groupby('nome_produto')['quantidade_vendida'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=vendas_por_produto.index, y=vendas_por_produto.values)
    plt.title('Total de Vendas por Produto')
    plt.xlabel('Produto')
    plt.ylabel('Quantidade Total Vendida')
    plt.xticks(rotation=45, ha='right') # Rotaciona os labels para melhor visualização
    plt.tight_layout() # Ajusta o layout para não cortar os labels
    plt.show() # Exibe o gráfico

if __name__ == '__main__':
    analisar_dados()