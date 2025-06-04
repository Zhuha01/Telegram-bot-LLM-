import os
import shutil

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

def clear_database(path="database"):
    if os.path.exists(path):
        shutil.rmtree(path)

files = {
    "cybersecurity": "information/cybersecurity.txt",
    "encryption": "information/encryption_methods.txt",
}

split = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator="\n")
embeddings = OpenAIEmbeddings()

clear_database()

all_texts = []

for topic, namefile in files.items():
    loader = TextLoader(namefile, encoding='utf-8')
    documents = loader.load()
    texts = split.split_documents(documents)
    for doc in texts:
        doc.metadata["topic"] = topic
    all_texts.extend(texts)

vectors = Chroma.from_documents(all_texts, embedding=embeddings, persist_directory="database")