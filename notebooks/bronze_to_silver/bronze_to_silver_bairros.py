import pandas as pd
import os
from shapely import wkt
from shapely.geometry import Polygon, MultiPolygon
from pyproj import Transformer

# Caminhos
bronze_path = '/Users/lucaslumertz/Documents/1Programacao/challanges/DESAFIO-PLACE/data/bronze/df_bairros_bronze.csv'
silver_path = '/Users/lucaslumertz/Documents/1Programacao/challanges/DESAFIO-PLACE/data/silver/df_bairros_silver.csv'

# Garante que a pasta silver existe
os.makedirs(os.path.dirname(silver_path), exist_ok=True)

# === 1. LEITURA ===
df = pd.read_csv(bronze_path, sep=',')

# === 2. REMOVER APENAS LINHAS SEM GEOMETRIA ===
df = df.dropna(subset=['GEOMETRIA'])

# === 3. PADRONIZAR NOMES DE COLUNAS ===
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

# === 4. PADRONIZAR TEXTOS ===
if 'nome' in df.columns:
    df['nome'] = df['nome'].astype(str).str.upper().str.strip()

# === 5. CONVERTER GEOMETRIA DE TEXTO PARA OBJETO GEOMÉTRICO ===
# Corrige strings mal formatadas (ex: falta de parênteses duplos)
df['geometria'] = df['geometria'].str.replace('MULTIPOLYGON ', 'MULTIPOLYGON', regex=False)
df['geometria'] = df['geometria'].str.replace('POLYGON ', 'POLYGON', regex=False)

# Converter texto WKT -> geometria shapely
def safe_wkt_load(wkt_str):
    try:
        return wkt.loads(wkt_str)
    except Exception:
        return None

df['geometry_obj'] = df['geometria'].apply(safe_wkt_load)

# === 6. CALCULAR CENTRÓIDE ===
df = df[df['geometry_obj'].notnull()].copy()
df['centroid'] = df['geometry_obj'].apply(lambda g: g.centroid if g else None)

# === 7. EXTRAIR COORDENADAS X/Y DO CENTRÓIDE ===
df['coord_x'] = df['centroid'].apply(lambda c: c.x if c else None)
df['coord_y'] = df['centroid'].apply(lambda c: c.y if c else None)

# === 8. CONVERTER PARA LATITUDE/LONGITUDE (EPSG:31983 → EPSG:4326) ===
transformer = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)
df['longitude'], df['latitude'] = transformer.transform(df['coord_x'].values, df['coord_y'].values)

# === 9. ORGANIZAR COLUNAS ===
colunas_coords = ['coord_y', 'coord_x', 'latitude', 'longitude']
outras = [col for col in df.columns if col not in colunas_coords + ['geometry_obj', 'centroid', 'geometria']]
df = df[outras + colunas_coords]

# === 10. SALVAR ===
df.to_csv(silver_path, sep=';', index=False)

print(f"✅ Arquivo SILVER salvo com sucesso em:\n{silver_path}")
print(f"Total de bairros processados: {df.shape[0]}")
