from .db import ConexaoBanco
from mysql.connector import Error

class DAO():
    def __init__(self):
        self.connection = ConexaoBanco().get_connection()
        self.cursor = self.connection.cursor()

    def atualizar(self, tabela: str, dados: str, where: str, valor_dados: tuple):
        try:
            sql = f"UPDATE {tabela} SET {dados} WHERE {where}"

            self.cursor.execute(sql, valor_dados)

            self.connection.commit()
            self.cursor.close()
        
        except Error as e:
            print()
            print(f"*ERRO! {e.msg}")
            print()
            print("- - - - - - - - - - - - - - - - - - - - - - ")
            print()
        finally:
            if self.connection.is_connected:
                self.connection.close()

    def inserir(self, tabela: str, dados: str, values: str, valor_dados: tuple):
        try:
            sql = f"INSERT INTO {tabela} ({dados}) VALUES ({values})"
            
            self.cursor.execute(sql, valor_dados)

            self.connection.commit()
            self.cursor.close()

        except Error as e:
            print()
            print(f"*ERRO! {e.msg}")
            print()
            print("- - - - - - - - - - - - - - - - - - - - - - ")
            print()
        finally:
            if self.connection.is_connected:
                self.connection.close()
        
    def visualizar(self, dados: str, tabela: str, where: str, valor_dados: tuple, one: bool):
        try:
            sql = f"SELECT {dados} FROM {tabela}{where}"

            if valor_dados == "":
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, valor_dados)
            
            if one:
                result = self.cursor.fetchone()
            else:
                result = self.cursor.fetchall()


            self.cursor.close()
            return result
        
        except Error as e:
            print()
            print(f"*ERRO! {e.msg}")
            print()
            print("- - - - - - - - - - - - - - - - - - - - - - ")
            print()
        finally:
            if self.connection.is_connected:
                self.connection.close()


# EXEMPLOS:

# Visualizar:
# filmes = dao_filmes.visualizar("id_filme, titulo", "filmes", "", "", False)
#     for i, filme in enumerate(filmes, start=1):
#         cx().filmes_db(i, filme[1], filme[0])

# dao_verificar_filme_db = dao()
# id_existe = dao_verificar_filme_db.visualizar("COUNT(*)", "filmes", 
# " WHERE id_filme = %s", (id_filme,), True)
# if id_existe[0] > 0:
#     print(f"Filme já foi carregado: {id_filme}")

# id_filmes = dao_pegar_id_filme.visualizar("id_filme", "elenco", 
# " WHERE nome = %s AND departamento = 'Acting'", (ator_info[0],), False)
# nome_filmes = []
# for id_filme in id_filmes:
#     dao_pegar_nome_filme = dao()
#     nome_filme = dao_pegar_nome_filme.visualizar("titulo", "filmes", 
# " WHERE id_filme = %s", (id_filme[0],), True)
#     nome_filmes.append(nome_filme[0])
# cx().info_atores_quantidade_filmes(ator_info[0], ator_info[1], nome_filmes)


# Inserir:
# dao_inserir_filme.inserir("filmes", "id_filme, titulo, revenue", 
# "%s, %s, %s", (data_info_filmes["id"], data_info_filmes["title"], 
# data_info_filmes["revenue"]))