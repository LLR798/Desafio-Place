import pandas as pd
import os

# === 1. LEITURA DO ARQUIVO ===
path = '/Users/lucaslumertz/Documents/1Programacao/challanges/DESAFIO-PLACE/data/input/20230502_bairro_oficial.csv' 

try:
    df = pd.read_csv(
        path, 
        sep=','
    )
    
    print(f"Arquivo lido com sucesso. Linhas lidas: {df.shape[0]}")
    print("\n--- Primeiras linhas lidas ---")
    print(df.head())

except FileNotFoundError:
    print(f"ERRO: O arquivo '{path}' não foi encontrado. Certifique-se de que ele foi carregado corretamente.")
    exit()
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo: {e}")
    exit()


# === 2. SALVAMENTO DO DATAFRAME ===
# Diretório de saída
output_dir = '/Users/lucaslumertz/Documents/1Programacao/challanges/PLACE v2/data/bronze'

# Garante que o diretório existe
os.makedirs(output_dir, exist_ok=True)

# Caminho completo do arquivo de saída
output_path = os.path.join(output_dir, 'df_bairros_bronze.csv')

# Salva com separador ; e índice começando em 1
df.to_csv(output_path, sep=',', index=True, index_label='ID')
df.index = df.index + 1

df.to_csv(output_path, sep=',', index=True, index_label='ID')

print(f"\nDataFrame salvo em '{output_path}' com {df.shape[0]} linhas (índice começa em 1, separador ',').")