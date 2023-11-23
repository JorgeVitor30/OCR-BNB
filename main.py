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
                if len(page[index_processo:(index_processo+39)].replace(' ', '')) > 30:
                    print(page.find('Processo'), page[index_processo:(index_processo+39)].replace(' ', ''))
                else:
                    print('ARQUIVO SEM NADA')


process = Ocr('publicacoes_42_90554530_221215_TJCE_20221215_085343.pdf')
process.returning_pages()
process.extraction()

#TODO FAZER UMA CLASSE DE VERIFICAÇÃO ARQUIVO WORD (CONVERSÃO PARA PDF)
