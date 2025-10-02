print("--- Checkpoint 1: O script app.py começou a ser lido. ---")

from flask import Flask, request, jsonify
import pandas as pd
import joblib

print("--- Checkpoint 2: Bibliotecas importadas. ---")

app = Flask(__name__)

print("--- Checkpoint 3: Aplicação Flask criada. ---")

try:
    modelo = joblib.load('modelo_vendas.pkl')
    print("--- Checkpoint 4: Modelo .pkl carregado com sucesso. ---")
except Exception as e:
    print(f"--- ERRO ao carregar o modelo: {e} ---")
    modelo = None

@app.route('/predict', methods=['POST'])
def predict():
    if modelo is None:
        return jsonify({'error': 'Modelo não foi carregado.'}), 500
    try:
        json_data = request.get_json()
        data = json_data['data']
        df = pd.DataFrame(data)

        df['data_da_previsao'] = pd.to_datetime(df['data_da_previsao'])
        df['ano'] = df['data_da_previsao'].dt.year
        df['mes'] = df['data_da_previsao'].dt.month
        df['dia'] = df['data_da_previsao'].dt.day
        df['dia_da_semana'] = df['data_da_previsao'].dt.dayofweek
        df['id_produto_num'] = df['id_produto'].astype('category').cat.codes

        features = ['ano', 'mes', 'dia', 'dia_da_semana', 'id_produto_num']

        previsoes = modelo.predict(df[features])

        return jsonify(previsoes.tolist())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

print("--- Checkpoint 5: Rota da API definida. ---")

if __name__ == '__main__':
    print("--- Checkpoint 6: Entrou no bloco de execução principal. INICIANDO SERVIDOR... ---")
    app.run(host='0.0.0.0', port=5000, debug=True)