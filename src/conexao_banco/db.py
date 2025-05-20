from mysql.connector import Error, connect
import time

from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST_CONNECT = os.getenv('DB_HOST_CONNECT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
class ConexaoBanco():
    def get_connection(self):
        connection = None
        for tentativa in range(10):
            try:
                connection = connect(
                    host=DB_HOST_CONNECT,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_DATABASE)
                return connection
            except Error as e:
                print(f"Tentativa {tentativa + 1}/10: Banco de dados não está pronto. Erro: {e}")
                time.sleep(5)
        print("Falha ao conectar ao banco de dados após 10 tentativas.")
        return None