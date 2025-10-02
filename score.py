import os
import json
import joblib
import pandas as pd

def init():
    global modelo
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'modelo_vendas.pkl')
    
    modelo = joblib.load(model_path)
    print("Modelo carregado com sucesso.")

def run(raw_data):
    try:
        print("Recebendo uma nova requisição...")
        data = json.loads(raw_data)['data']
        
        df = pd.DataFrame(data)
        
        df['data_da_previsao'] = pd.to_datetime(df['data_da_previsao'])
        df['ano'] = df['data_da_previsao'].dt.year
        df['mes'] = df['data_da_previsao'].dt.month
        df['dia'] = df['data_da_previsao'].dt.day
        df['dia_da_semana'] = df['data_da_previsao'].dt.dayofweek
        df['id_produto_num'] = df['id_produto'].astype('category').cat.codes

        features = ['ano', 'mes', 'dia', 'dia_da_semana', 'id_produto_num']
        
        previsoes = modelo.predict(df[features])
        
        print("Previsão realizada com sucesso.")
        return json.dumps(previsoes.tolist())

    except Exception as e:
        error = str(e)
        return json.dumps({'error': error})