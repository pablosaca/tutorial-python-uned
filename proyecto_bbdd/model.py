import pandas as pd
from apply_db import load_config_file
from src.database.db_connect import DataBaseProject

config_file = load_config_file()  # lee fichero de configuración
# Instanciamos la clase de DB
db = DataBaseProject(db_name=config_file["db_name"])
db.db_connect()  # conecta la database (si no está creada, se crea en el momento)

# TODO PSC: debuggear para enseñar que se guardan los dos tablones
train_query = f"""SELECT * FROM {config_file['tables']['model_data']}"""
train_df = pd.read_sql_query(train_query, db.connection)