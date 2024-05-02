import yaml
import pandas as pd
from src.database.db_connect import DataBaseProject


def load_config_file(filepath: str = "config/config.yaml"):
    with open(filepath, "r") as f:
        config_data = yaml.safe_load(f)
    return config_data


def load_data(filepath: str = "data/marketing_campaing.parquet"):
    df = pd.read_parquet(filepath)
    return df


def get_train_test_data(config_data: dict, data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    
    :param config_data: dict
    :param data: pd.DataFrame
    :return tuple(pd.DataFrames): train y test tables
    """
    column = config_data["filters"]["train_test_data"]["col"]
    threshold = config_data["filters"]["train_test_data"]["threshold"]

    train_data = data[data[column] < threshold]
    test_data = data[data[column] >= threshold]
    return train_data, test_data


def save_original_table_in_db():
    """

    :param config_data:
    :param table_name:
    :return:
    """

    config_file = load_config_file()  # lee fichero de configuración
    df = load_data()  # lee datos de mercado

    # Instanciamos la clase de DB
    db = DataBaseProject(db_name=config_file["db_name"])
    db.db_connect()  # conecta la database (si no está creada, se crea en el momento)

    db.write_table(df=df, table_name=config_file["tables"]["data"])  # escribe la tabla en bbdd

    # TODO PSC: debuggear para enseñar que los datos se guardan
    # podemos ver los datos cargados
    query = f"""SELECT * FROM {config_file['tables']['data']}"""
    data = pd.read_sql_query(query, db.connection)

    # obtención de las muestras de train y test y se guardan en la database
    train_data, test_data = get_train_test_data(config_data=config_file, data=data)
    db.write_table(df=train_data, table_name=config_file["tables"]["model_data"])  # escribe la tabla de train
    db.write_table(df=test_data, table_name=config_file["tables"]["pred_data"])  # escribe la tabla de train

    # TODO PSC: debuggear para enseñar que se guardan los dos tablones
    # train_query = f"""SELECT * FROM {config_file['tables']['model_data']}"""
    # pd.read_sql_query(train_query, db.connection).shape

    # test_query = f"""SELECT * FROM {config_file['tables']['pred_data']}"""
    # pd.read_sql_query(test_query, db.connection).shape

    # print("adios...")


save_original_table_in_db()



