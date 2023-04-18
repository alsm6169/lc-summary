import re

from PyPDF2 import PdfReader


# This function is reading PDF from the start page to final page
# given as input (if less pages exist, then it reads till this last page)
def get_pdf_text(document_path, start_page=1, final_page=999):
    reader = PdfReader(document_path)
    number_of_pages = len(reader.pages)
    print(f'numer of pages: {number_of_pages}')
    # pages = '\npages#' + str(start_page) + '\n'
    pages = ''
    pattern = 'Show Notes:  http://www.superdatascience.com/\d+\s*\d+'
    for page_num in range(start_page - 1, min(number_of_pages, final_page)):
        page = reader.pages[page_num].extract_text()
        page = re.sub(pattern,' ',page).strip()

        pages += page
        # pages += '\n\npages#' + str(page_num + 2) + ' \n' if page_num < final_page - 1 else ''
    return pages


if __name__ == '__main__':
    doc_path_name = 'documents/PT667-Transcript.pdf'
    doc_text = get_pdf_text(doc_path_name, 2)
    print(doc_text)
