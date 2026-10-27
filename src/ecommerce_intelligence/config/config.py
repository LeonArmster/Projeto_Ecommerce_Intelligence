# ==================================
# Arquivo de configuração e direcionamento de pastas
# ==================================
import os
from pathlib import Path
from dotenv import load_dotenv

# Caminho principal
main_dir = Path(__file__).parent.parent.parent.parent

# Caminho dos arquivos
data_dir = main_dir/'data'
processed_dir = data_dir/'processed'
raw_dir = data_dir/'raw'
sample_dir = data_dir/'samples'

# Caminho do sql
sql_dir = main_dir/'sql'


# Caminho do log
log_dir = main_dir/'logs'


# Carregando o env dos dados
load_dotenv()


pg_host=os.getenv("POSTGRES_HOST")
pg_port=os.getenv("POSTGRES_PORT")
pg_dbname=os.getenv("POSTGRES_DB")
pg_user=os.getenv("POSTGRES_USER")
pg_password=os.getenv("POSTGRES_PASSWORD")

