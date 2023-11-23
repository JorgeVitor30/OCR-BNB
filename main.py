import pandas as pd
from PyPDF2 import PdfReader

class Ocr:
    def __init__(self, dir_pdf):
        self.dir = dir_pdf
        self.pdf = PdfReader(dir_pdf)

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
                titulo = page[index_titulo:]

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
        df = pd.DataFrame(lista, columns=colunas)
        print(df)
        df.to_excel('teste.xlsx')

process = Ocr('publicacoes_42_90554530_221215_TJCE_20221215_085343.pdf')
process.process()



#TODO FAZER UMA CLASSE DE VERIFICAÇÃO ARQUIVO WORD (CONVERSÃO PARA PDF)
