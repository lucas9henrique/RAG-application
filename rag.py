import fitz  # PyMuPDF
import os

# Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Função para extrair texto de todos os PDFs em uma pasta
def extract_texts_from_folder(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            texts.append(text)
    return texts

# Caminho para a pasta contendo os PDFs
folder_path = ".\docs"
pdf_texts = extract_texts_from_folder(folder_path)

# Criando um DataFrame com os textos extraídos
import pandas as pd

data = pd.DataFrame({'report_text': pdf_texts})

# Exibir as primeiras linhas do dataframe para verificar os textos extraídos
print(data.head())
