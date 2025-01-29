import os
import importlib


def run_migrations():
    migration_files = sorted(f for f in os.listdir(os.path.dirname(__file__)) if f.startswith("migration_") and f.endswith(".py"))
    
    for file in migration_files:
        module_name = f"migrations.{file[:-3]}"  # Remove ".py" do nome do arquivo
        migration_module = importlib.import_module(module_name)
        print(f"🔄 Executando {file}...")
        migration_module.migrate()
        print(f"✅ {file} aplicada com sucesso!\n")

if __name__ == "__main__":
    run_migrations()
