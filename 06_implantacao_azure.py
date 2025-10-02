import datetime
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
)

ml_client = MLClient.from_config(DefaultAzureCredential())

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
endpoint_name = f"previsao-vendas-{timestamp}"
deployment_name = "blue" 

print("Registrando o modelo...")
model_local_path = "modelo_vendas.pkl"
model = Model(
    path=model_local_path,
    name="modelo-previsao-vendas",
    description="Modelo RandomForest para prever vendas.",
    type="custom_model",
)
registered_model = ml_client.models.create_or_update(model)
print(f"Modelo registrado com sucesso: {registered_model.name} versão {registered_model.version}")

print("Definindo o ambiente...")
env = Environment(
    name="env-previsao-vendas",
    description="Ambiente para o modelo de previsão de vendas.",
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest",
    conda_file={
        "channels": ["conda-forge"],
        "dependencies": [
            "python=3.8",
            "pip",
            {
                "pip": ["pandas", "scikit-learn==1.2.2", "joblib", "azureml-defaults"]
            },
        ],
    },
)

print("Configurando o endpoint e a implantação...")
endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    description="Endpoint para o modelo de previsão de vendas.",
    auth_mode="key",
)

deployment = ManagedOnlineDeployment(
    name=deployment_name,
    endpoint_name=endpoint_name,
    model=registered_model,
    environment=env,
    code_configuration=CodeConfiguration(
        code="./",  
        scoring_script="score.py",
    ),
    instance_type="Standard_DS2_v2",
    instance_count=1,
)

print("Iniciando a criação do endpoint... Isso pode levar de 10 a 20 minutos.")
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

print("Iniciando a implantação do modelo no endpoint... Isso também pode demorar.")
ml_client.online_deployments.begin_create_or_update(deployment).result()

print("\nImplantação concluída com sucesso!")
print(f"Endpoint '{endpoint_name}' está pronto para receber requisições.")