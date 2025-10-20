import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
import os

# === 1. Caminhos dos arquivos SILVER ===
path_empresas = '/Users/lucaslumertz/Documents/1Programacao/challanges/PLACE v2/data/silver/df_empresas_silver.csv'
path_bairros = '/Users/lucaslumertz/Documents/1Programacao/challanges/PLACE v2/data/silver/df_bairros_silver.csv'
path_onibus = '/Users/lucaslumertz/Documents/1Programacao/challanges/PLACE v2/data/silver/df_pontos_onibus_silver.csv'

# === 2. Leitura dos arquivos ===
df_empresas = pd.read_csv(path_empresas, sep=';')
df_bairros = pd.read_csv(path_bairros, sep=';')
df_onibus = pd.read_csv(path_onibus, sep=';')

# === 3. Empresas por bairro ===
empresas_por_bairro = df_empresas.groupby('nome_bairro').size().reset_index(name='qtd_empresas')
df_bairros = df_bairros.merge(empresas_por_bairro, how='left', left_on='nome', right_on='nome_bairro')
df_bairros['qtd_empresas'] = df_bairros['qtd_empresas'].fillna(0).astype(int)
df_bairros.drop(columns=['nome_bairro'], inplace=True)

# === 4. Limpeza de coordenadas inválidas ===
df_onibus = df_onibus[
    df_onibus['latitude'].between(-90, 90) & df_onibus['longitude'].between(-180, 180)
]

# === 5. Construção do BallTree (pontos de ônibus) ===
bairros_coords = np.radians(df_bairros[['latitude', 'longitude']])
onibus_coords = np.radians(df_onibus[['latitude', 'longitude']])
onibus_tree = BallTree(onibus_coords, metric='haversine')

# Raio de 500 metros em radianos
raio_metros = 500
raio_radianos = raio_metros / 6371000

# Contar pontos de ônibus ao redor do centro do bairro (raio de 500m)
qtd_onibus_por_bairro = onibus_tree.query_radius(bairros_coords, r=raio_radianos, count_only=True)
df_bairros['qtd_pontos_onibus'] = qtd_onibus_por_bairro

# === 6. Cálculo de densidades ===
df_bairros['empresas_por_km2'] = df_bairros['qtd_empresas'] / df_bairros['area_km2']
df_bairros['pontos_onibus_por_km2'] = df_bairros['qtd_pontos_onibus'] / df_bairros['area_km2']

# === 7. Cálculo do novo potencial_score com pesos ===
z_empresas = (df_bairros['empresas_por_km2'] - df_bairros['empresas_por_km2'].mean()) / df_bairros['empresas_por_km2'].std()
z_onibus = (df_bairros['pontos_onibus_por_km2'] - df_bairros['pontos_onibus_por_km2'].mean()) / df_bairros['pontos_onibus_por_km2'].std()

# Score ponderado com 40% empresas e 60% transporte
score_raw = (0.4 * z_empresas + 0.6 * z_onibus)

# Normaliza o score para uma escala de 0 a 10
score_min = score_raw.min()
score_max = score_raw.max()
score_normalizado = (score_raw - score_min) / (score_max - score_min) * 10

# Armazena com duas casas decimais
df_bairros['potencial_score'] = score_normalizado.round(2)


# === 8. Classificação do score ===
def classificar_score(score):
    if score >= 2:
        return 'Ótimo'
    elif 1 <= score < 2:
        return 'Bom'
    elif -1 <= score < 1:
        return 'Potencial'
    elif -2 <= score < -1:
        return 'Neutro'
    else:
        return 'Arriscado'


df_bairros['categoria_score'] = df_bairros['potencial_score'].apply(classificar_score)



# === 9. Renomear 'nome' para 'nome_do_bairro' ===
df_bairros.rename(columns={'nome': 'nome_do_bairro'}, inplace=True)

# === 10. Seleção das colunas finais ===
df_gold = df_bairros[[
    'nome_do_bairro', 'tipo', 'area_km2', 'qtd_empresas', 'qtd_pontos_onibus',
    'empresas_por_km2', 'pontos_onibus_por_km2', 'potencial_score',
    'categoria_score', 'latitude', 'longitude'
]].sort_values(by='potencial_score', ascending=False)

# === 11. Salvamento da camada GOLD ===
output_path = '/Users/lucaslumertz/Documents/1Programacao/challanges/PLACE v2/data/gold/regioes_promissoras_gold.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_gold.to_csv(output_path, sep=';', index=False)

print(f"✅ Camada GOLD gerada e salva com sucesso em:\n{output_path}")
print(f"Total de registros processados: {df_gold.shape[0]}")