import pandas as pd
import os
from pyproj import Transformer

# Caminhos dos arquivos
bronze_path = '/Users/lucaslumertz/Documents/1Programacao/challanges/PLACE v2/data/bronze/df_pontos_onibus_bronze.csv'
silver_path = '/Users/lucaslumertz/Documents/1Programacao/challanges/PLACE v2/data/silver/df_pontos_onibus_silver.csv'

# Cria a pasta silver se não existir
os.makedirs(os.path.dirname(silver_path), exist_ok=True)

# === 1. LEITURA DO ARQUIVO ===
df = pd.read_csv(bronze_path, sep=';')

# === 2. REMOVER APENAS LINHAS SEM GEOMETRIA ===
df = df.dropna(subset=['GEOMETRIA'])

# === 3. PADRONIZAÇÃO DOS NOMES DAS COLUNAS ===
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('ã', 'a')
    .str.replace('ç', 'c')
    .str.replace('é', 'e')
    .str.replace('í', 'i')
)

# === 4. PADRONIZAÇÃO DE TEXTOS ===
for col in ['nome_linha', 'nome_sub_linha', 'origem']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.upper().str.strip()

# === 5. EXTRAÇÃO DAS COORDENADAS X/Y (em metros - UTM) ===
df[['coord_x', 'coord_y']] = df['geometria'].str.extract(r'POINT\s*\((.*?)\s+(.*?)\)').astype(float)

# === 6. CONVERSÃO DE COORDENADAS (UTM → LAT/LON WGS84) ===
# EPSG:31983 = SIRGAS 2000 / UTM zone 23S (região de Belo Horizonte)
# EPSG:4326 = WGS84 (latitude/longitude global)
transformer = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)

lon, lat = transformer.transform(df['coord_x'].values, df['coord_y'].values)

# === 7. ADICIONAR LAT/LON E REORDENAR PARA PADRÃO DE MAPAS (Y antes de X) ===
df['latitude'] = lat
df['longitude'] = lon

# Reordena as colunas de coordenadas para o padrão GIS
colunas_ordem = ['coord_y', 'coord_x', 'latitude', 'longitude']
outras_colunas = [c for c in df.columns if c not in colunas_ordem]
df = df[outras_colunas + colunas_ordem]

# === 8. LIMPEZA FINAL ===
df = df.drop(columns=['geometria'])
df = df.drop_duplicates()

# === 9. SALVAMENTO ===
df.to_csv(silver_path, sep=';', index=False)

print(f"✅ Arquivo da camada SILVER salvo com sucesso em:\n{silver_path}")
print(f"Total de pontos de ônibus processados: {df.shape[0]}")