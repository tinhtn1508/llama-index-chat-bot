import chromadb
import os
import tqdm
import json
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

def load_embedding(documents_directory: str, collection_name: str, persist_directory: str, embedding_type: str) -> None:
    documents = []
    metadatas = []
    files = os.listdir(documents_directory)
    for file in tqdm.tqdm(files, desc='Reading documents'):
        file_path = os.path.join(documents_directory, file)
        doc, meta = chunking_document(file_path, 'line')
        for d in doc:
            documents.append(d)
        for m in meta:
            metadatas.append(m)
    client = chromadb.PersistentClient(path=persist_directory)
    embedding_function = get_embedding_function(embedding_type)
    collection_name = collection_name if embedding_type == 'google' else collection_name +  "_" + embedding_type
    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_function
    )
    count = collection.count()
    print(f"Collection already contains {count} documents")
    ids = [str(i) for i in range(count, count + len(documents))]
    for i in tqdm.tqdm(range(0, len(documents), 100), desc="Adding documents", unit_scale=100):
        collection.add(
            ids=ids[i : i + 100],
            documents=documents[i : i + 100],
            metadatas=metadatas[i : i + 100],
        )
    new_count = collection.count()
    print(f"Added {new_count - count} documents")

def chunking_document(filename: str, chunking_type: str) -> list:
    documents = []
    metadata = []
    with open(filename, 'r') as f:
        raw_text = json.load(f)
    text_content = raw_text['text_content']
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n', '.'],
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_text(text_content)
    for i, text in enumerate(texts):
        documents.append(text)
        metadata.append({
            'title': raw_text['meta']['title'],
            'url': raw_text['meta']['url'],
            'date': raw_text['meta']['date'],
            'chunk_id': i,
        })
    return documents, metadata

def get_embedding_function(embedding_type: str) -> embedding_functions.EmbeddingFunction:
    if embedding_type == 'google':
        return embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=config.conf['google_api_key']
        )
    elif embedding_type == 'onnx':
        return embedding_functions.ONNXMiniLM_L6_V2()
    elif embedding_type == 'huggingface':
        return embedding_functions.HuggingFaceEmbeddingFunction(
            api_key=config.conf['huggingface_api_key']
        )
    elif embedding_type == 'transformer':
        return embedding_functions.SentenceTransformerEmbeddingFunction()
    else:
        raise ValueError('Invalid embedding type')