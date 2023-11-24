import os
import pandas as pd
import win32com.client

from PyPDF2 import PdfReader


class Ocr:
    def __init__(self):
        self.pdf = self.opening_file()

    def process(self):
        dados = self.extraction()
        self.transform_to_df(dados)

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
                index_data_publi3 = page.find('Data Pub')
                index_data_publi4 = page.find('DataPublicação::')

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

                id_compromisso = id_processo + ' ' + data_dispo


                data_publi = page[index_data_publi+number_aux_publi:index_jornal].strip()
                jornal = page[index_jornal+7:index_tribunal].strip()
                tribunal = page[index_tribunal+9:index_vara].strip()
                vara = page[index_vara + 5:index_cidade].strip()
                cidade = page[index_cidade+7:index_pagina].strip()
                pagina = page[index_pagina+7:index_titulo].strip()
                titulo = page[index_titulo+7:].strip()

                temp_aux.append(id_compromisso)
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

        colunas = ["id_compromisso", "data_publicacao", "jornal", "tribunal", "vara", "cidade", "pagina", "titulo"]
        df = pd.DataFrame(lista, columns=colunas).set_index('id_compromisso')
        # print(df)
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

try:
    process = Ocr()
    process.process()
except Exception as e:
    raise e


#TODO FAZER UMA CLASSE DE VERIFICAÇÃO ARQUIVO WORD (CONVERSÃO PARA PDF)
