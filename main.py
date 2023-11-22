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
        # Extração dos dados do PDF
        pass



process = Ocr('publicacoes_42_90554530_221215_TJCE_20221215_085343.pdf')
process.returning_pages()

#TODO FAZER UMA CLASSE DE VERIFICAÇÃO ARQUIVO WORD (CONVERSÃO PARA PDF)
