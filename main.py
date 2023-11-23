from PyPDF2 import PdfReader

class Ocr:
    def __init__(self, dir_pdf):
        self.dir = dir_pdf
        self.pdf = PdfReader(dir_pdf)

    def process(self):
        # Onde todos os processos são interligados
        pass

    def returning_pages(self):
        # Quantidade total de páginas no PDF
        qtd_page = 0
        page = self.pdf.pages
        for i, x in enumerate(page):
            qtd_page = i

        return qtd_page

    def extraction(self):

        for i in range(2):
            page = self.pdf.pages[i].extract_text()

            validate_page = page.find('BANCO DO NORDESTE')

            if validate_page != -1:
                list_data = []

                index_processo = page.find('Processo')
                index_data_disp = page.find('Data Disponibilização::')
                index_data_publi = page.find('Data Publicação::')
                index_jornal = page.find('Jornal:')
                index_tribunal = page.find('Tribunal:')
                index_vara = page.find('Vara:')
                index_cidade =page.find('Cidade:')
                index_pagina = page.find('Página:')
                index_titulo = page.find('Título:')


                id_processo = page[(index_processo+9):index_data_disp].replace(' ', '').strip()

                data_dispo = page[index_data_disp+23:index_data_publi].strip()

                id_compromisso = id_processo + ' ' + data_dispo

                print(id_compromisso)

                data_publi = page[index_data_publi+17:index_jornal].strip()
                print(data_publi)

                jornal = page[index_jornal+7:index_tribunal].strip()
                print(jornal)

                tribunal = page[index_tribunal+9:index_vara].strip()
                print(tribunal)

                vara = page[index_vara + 5:index_cidade].strip()
                print(vara)

                cidade = page[index_cidade+7:index_pagina].strip()
                print(cidade)

                pagina = page[index_pagina+7:index_titulo].strip()
                print(pagina)

                titulo = page[index_titulo:]
                print(titulo)


                print('\n')





process = Ocr('publicacoes_42_90554530_221215_TJCE_20221215_085343.pdf')
process.returning_pages()
process.extraction()

#TODO FAZER UMA CLASSE DE VERIFICAÇÃO ARQUIVO WORD (CONVERSÃO PARA PDF)
