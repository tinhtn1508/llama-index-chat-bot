import os
from typing import List

import google.generativeai as genai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
import chromadb
import config
import embedding
import backoff

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


def server(collection_name: str = "documents_collection", persist_directory: str = ".", embedding_type: str = 'google', llm: str = 'gemini') -> None:
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
        response = generate_response(build_prompt(query, results["documents"][0]), llm)
        print(response)
        print("\n")
        print(f"Source documents:\n{sources}")
        print("\n")

@backoff.on_exception(backoff.constant, ValueError, interval=1, max_tries=5)
def generate_response(prompt: str, llm: str) -> str:
    if llm == 'gemini':
        model = genai.GenerativeModel("gemini-pro")
        genai.configure(api_key=config.conf["google_api_key"])
        response = model.generate_content(prompt).text
        return response
    elif llm == 'openai':
        client = OpenAI(api_key=config.conf["openai_api_key"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"{prompt}"},
            ]
        )
        return response.choices[0].message.text
    elif llm == 'mistral':
        client = MistralClient(api_key=config.conf["mistral_api_key"])
        chat_response = client.chat(
            model="mistral-large-latest",
            messages=[ChatMessage(role="user", content=f"{prompt}")],
        )
        return chat_response.choices[0].message.content
    else:
        raise ValueError("Invalid LLM model")