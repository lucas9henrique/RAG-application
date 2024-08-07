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


import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from transformers import pipeline
from rank_bm25 import BM25Okapi
import fitz  # PyMuPDF

# Baixando recursos necessários para nltk
nltk.download('punkt')

# Função para extrair texto de PDFs
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Preparação dos dados
data = pd.DataFrame({'report_text': [pdf_texts]})  # Adiciona o texto extraído do PDF ao DataFrame

# Função para pré-processar o texto
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum()]
    return tokens

# Aplicando a função de pré-processamento aos textos
data['tokens'] = data['report_text'].apply(lambda x: preprocess_text(x))

# Criando o modelo BM25
bm25 = BM25Okapi(data['tokens'].tolist())

# Função para recuperação de documentos relevantes
def retrieve_documents(query, bm25_model, data, top_n=5):
    query_tokens = preprocess_text(query)
    scores = bm25_model.get_scores(query_tokens)
    top_n_indices = scores.argsort()[-top_n:][::-1]
    return data.iloc[top_n_indices]

# Exemplo de uso para recuperação de documentos
query = "engine failure during flight"
retrieved_docs = retrieve_documents(query, bm25, data)
print(retrieved_docs[['report_text']])

# Carregando o modelo de linguagem
generator = pipeline('text-generation', model='gpt-3.5-turbo')

# Função para gerar respostas
def generate_answer(query, retrieved_docs, generator_model):
    context = " ".join(retrieved_docs['report_text'].tolist())
    input_text = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    response = generator_model(input_text, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']

# Exemplo de uso para geração de resposta
answer = generate_answer(query, retrieved_docs, generator)
print(answer)