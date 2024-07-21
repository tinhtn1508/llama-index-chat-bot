import os
from typing import List

import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
import config
import embedding

def build_prompt(query: str, context: List[str]) -> str:
    context = " ".join(context)
    prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
    strike a friendly and converstional tone. \
    If the passage is irrelevant to the answer, you may ignore it.
    QUESTION: '{query}'
    PASSAGE: '{context}'
    ANSWER:
    """).format(query=query, context=context)
    return prompt


def server(collection_name: str = "documents_collection", persist_directory: str = ".", embedding_type: str = 'google') -> None:
    model = genai.GenerativeModel("gemini-pro")
    genai.configure(api_key=config.conf["google_api_key"])
    client = chromadb.PersistentClient(path=persist_directory)
    embedding_function = embedding.get_embedding_function(embedding_type)
    collection_name = collection_name if embedding_type == 'google' else collection_name + "_" + embedding_type
    collection = client.get_collection(
        name=collection_name, embedding_function=embedding_function
    )
    while True:
        query = input("Question: ")
        if len(query) == 0:
            print("Please enter a question. Ctrl+C to Quit.\n")
            continue
        print("\nThinking...\n")
        results = collection.query(query_texts=[query], n_results=5, include=["documents", "metadatas"])

        sources = "\n".join(
            [
                f"URL: {result['url']} - Chunk_id: {result['chunk_id']}"
                for result in results["metadatas"][0]  # type: ignore
            ]
        )
        response = model.generate_content(build_prompt(query, results["documents"][0])).text
        print(response)
        print("\n")
        print(f"Source documents:\n{sources}")
        print("\n")
