import os
import subprocess

# Caminhos base
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# === 1. Load para Bronze ===
print("🚀 Executando etapa: LOAD → BRONZE")

subprocess.run([
    "python",
    os.path.join(BASE_PATH, "notebooks/load_to_bronze/load_bairros_to_bronze.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE_PATH, "notebooks/load_to_bronze/load_empresas_to_bronze.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE_PATH, "notebooks/load_to_bronze/load_pontos_onibus_to_bronze.py")
], check=True)


# === 2. Bronze → Silver ===
print("🔄 Executando etapa: BRONZE → SILVER")

subprocess.run([
    "python",
    os.path.join(BASE_PATH, "notebooks/bronze_to_silver/bronze_to_silver_bairros.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE_PATH, "notebooks/bronze_to_silver/bronze_to_silver_empresas.py")
], check=True)

subprocess.run([
    "python",
    os.path.join(BASE_PATH, "notebooks/bronze_to_silver/bronze_to_silver_ponto_onibus.py")
], check=True)


# === 3. Silver → Gold ===
print("🏁 Executando etapa: SILVER → GOLD")

subprocess.run([
    "python",
    os.path.join(BASE_PATH, "notebooks/silver_to_gold/silver_to_gold.py")
], check=True)

print("✅ Pipeline ETL concluído com sucesso!")
