import os
import pandas as pd
import win32com.client

from PyPDF2 import PdfReader
from connection import ConnectionDb


class Ocr:
    def __init__(self):
        self.pdf = self.opening_file()

    def process(self):
        dados = self.extraction()
        df = self.transform_to_df(dados)
        self.insert_to_db_sql(df)

    def returning_pages(self):
        # Quantidade total de páginas no PDF
        qtd_page = 0
        page = self.pdf.pages
        for i, x in enumerate(page):
            qtd_page = i

        return qtd_page

    def extraction(self):
        all_list = []
        for i in range(self.returning_pages()):
            temp_aux = []
            page = self.pdf.pages[i].extract_text()

            validate_page = page.find('BANCO DO NORDESTE')

            if validate_page != -1:

                index_processo = page.find('Processo')
                index_data_disp = page.find('Data Disponibilização::')

                index_data_publi = page.find('Data Publicação::')
                index_data_publi2 = page.find('Data Publ')

                index_jornal = page.find('Jornal:')
                index_tribunal = page.find('Tribunal:')
                index_vara = page.find('Vara:')
                index_cidade =page.find('Cidade:')
                index_pagina = page.find('Página:')
                index_titulo = page.find('Título:')

                number_aux_publi = 17

                if index_data_publi == -1:
                    index_data_publi = index_data_publi2
                    number_aux_publi += 1

                id_processo = page[(index_processo+9):index_data_disp].replace(' ', '').strip()
                data_dispo = page[index_data_disp+23:index_data_publi].strip()

                data_publi = page[index_data_publi+number_aux_publi:index_jornal].strip()
                jornal = page[index_jornal+7:index_tribunal].strip()
                tribunal = page[index_tribunal+9:index_vara].strip()
                vara = page[index_vara + 5:index_cidade].strip()
                cidade = page[index_cidade+7:index_pagina].strip()
                pagina = page[index_pagina+7:index_titulo].strip()
                titulo = page[index_titulo+7:].strip()

                temp_aux.append(id_processo)
                temp_aux.append(data_dispo)
                temp_aux.append(data_publi)
                temp_aux.append(jornal)
                temp_aux.append(tribunal)
                temp_aux.append(vara)
                temp_aux.append(cidade)
                temp_aux.append(pagina)
                temp_aux.append(titulo)

                all_list.append(temp_aux)

        return all_list

    def transform_to_df(self, lista):
        df = pd.DataFrame()

        colunas = ["id_compromisso", "data_disponibilizacao", "data_publicacao", "jornal", "tribunal", "vara", "cidade", "pagina", "titulo"]
        df = pd.DataFrame(lista, columns=colunas)

        df.to_excel('teste.xlsx')

        return df

    def opening_file(self):
        caminho = R'C:\Users\B901488\OneDrive - bnb.gov.br\Documentos\PASTA_OCR'
        file_name = os.listdir(caminho)[0]
        if '.pdf' in file_name:
            pdf = PdfReader(f'{caminho}\\' + file_name)

            return pdf

        if '.doc' in file_name:
            wdFormatPDF = 17

            inputFile = os.path.abspath(f"{caminho}\\{file_name}")
            outputFile = os.path.abspath(f"{caminho}\\{file_name}.pdf")
            word = win32com.client.Dispatch("Word.Application")
            doc = word.Documents.Open(inputFile)
            doc.SaveAs(outputFile, FileFormat=wdFormatPDF)
            doc.Close()
            word.Quit()

            pdf = PdfReader(f'{caminho}\\{file_name}.pdf')

            return pdf

        return False

    def insert_to_db_sql(self, df):
        import pyodbc

        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=G03SQLD01\DWD;DATABASE=B901488;Trusted_Connection=yes;')

        try:
            cursor = conn.cursor()

            cursor.execute('TRUNCATE TABLE Intimacao')

            for index, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO Intimacao (id_compromisso, data_disponibilizacao, data_publicacao, jornal, vara, cidade, pagina, titulo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               row['id_compromisso'], row['data_disponibilizacao'],row['data_publicacao'], row['jornal'], row['vara'], row['cidade'], row['pagina'], row['titulo'])

            conn.commit()
            print("Operação realizada com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Ocorreu um erro: {str(e)}")

        # Feche a conexão

        conn.close()


try:
    process = Ocr()
    process.process()
except Exception as e:
    raise e
