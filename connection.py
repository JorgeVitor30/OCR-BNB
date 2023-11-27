import pyodbc
import pandas

class ConnectionDb:
    def __init__(self, df):
        self.conn = pyodbc.connect('Driver={SQL Server};'
        'Server=G03SQLD01\DWD;'
        'Database=B901488;'
        'Trusted_Connection=yes;')
        self.df = df


    def insert_to_db(self):
        cursor = self.conn.cursor()

        print(self.df['titulo'])

        if self.df is not None:

            for i, infos in self.df.iterrows():
                print(infos[6])
                inserir_dados = f"""
                        INSERT INTO intimicacao (id_compromisso, data_publicacao, jornal, vara, cidade, pagina, titulo)
                        VALUES (
                        '{infos[0]}',
                        '{infos[1]}',
                        '{infos[2]}',
                        '{infos[3]}',
                        '{infos[4]}',
                        '{infos[5]}',
                        '{infos[6]}',
                        """
                print(inserir_dados)

                cursor.execute(inserir_dados)
                self.conn.commit()

        cursor.close()

        self.conn.close()
