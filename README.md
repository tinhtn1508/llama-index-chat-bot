# llama-index-chat-bot

## Problem

Using OpenAI/Gemini/Claude API or open-source LLMs models, combined with the knowledge learned about RAG techniques, to build a Chatbot application that accurately answers questions related to all the articles on the llama-index blog: https://www.llamaindex.ai/blog.

## Prerequisite

Python version: 3.12.3

Install dependencies
```
pip install -r requirements.txt
```

Setup environment, go to the `config.json` in `config` folder and fill the necessary api keys.
```
"crawler": {
    "jina_api_key": "",
    "data_path": "data"
},
"google_api_key": "",
"huggingface_api_key": "",
"openai_api_key": "",
"mistral_api_key": ""
```


## How to start

There are two options for you:
- **Build from scratch**: Firstly you must delete the `chroma_storage` folder, then go through 3 steps below.
- **Only start bot server for ask and answer**.  I highly recommend this approach to save time. I have already crawled and embedded the data in some ways. Please bypass steps 1 and 2 and go directly to step 3.


### 1. How to crawl data

```
python3 main.py --type crawler
```
### 2. How to embed data

Support embedding: `google`, `onnx`, `huggingface` and `transformer`. Corresponding `models/embedding-gecko-001`, `all-MiniLM-L6-v2`, `sentence-transformers/all-MiniLM-L6-v2` and `all-MiniLM-L6-v2` embedding model.

Support chunking: `RecursiveCharacterTextSplitter` and `SentenceTransformersTokenTextSplitter`


```
python3 main.py --type embedding --embedding_type onnx --chunking_type recursive_character
```

or

```
python3 main.py --type embedding --embedding_type onnx --chunking_type sentence_transformers_token
```

### 3. How ask question 

Support LLM: `mistral`, `openai` (`gpt-4o-mini` model) and `gemini`. 

After many experiments, the following parameters are suitable for getting a good answer from the bot:

```
python3 main.py --type server --embedding_type onnx --chunking_type sentence_transformers_token --llm mistral --display_source true
```

Additionally, you can change the above parameters to see different answers from the bot, like this:

```
python3 main.py --type server --embedding_type onnx --chunking_type sentence_transformers_token --llm gemini --display_source true
```

or 

```
python3 main.py --type server --embedding_type onnx --chunking_type recursive_character --llm mistral --display_source true
```


### There are some question and answer from chat-bot

Question 1

```
Question: What are key features of llama-agents?

Thinking...

Sure, let's break it down! Llama-agents is a powerful framework designed to help you build complex multi-agent AI systems. Here are some key features that make it stand out:

1. **Distributed Service-Oriented Architecture**: Each agent in Llama-agents can run independently as its own microservice. These agents are coordinated by a customizable control plane powered by a large language model (LLM), which routes and distributes tasks efficiently.

2. **Communication via Standardized API Interfaces**: Agents communicate with each other through a central control plane orchestrator. They pass messages back and forth using a message queue, making the system organized and easy to manage.

3. **Define Agentic and Explicit Orchestration Flows**: Developers have the flexibility to either directly define how agents interact or let an "agentic orchestrator" decide which agents are relevant to a task. This provides a lot of control and adaptability.

4. **Ease of Deployment**: You can launch, scale, and monitor each agent and the control plane independently. This makes it easier to manage and scale your system as needed.

5. **Scalability and Resource Management**: Llama-agents comes with built-in observability tools to monitor the quality and performance of the system and each individual agent service. This helps ensure everything runs smoothly and efficiently.

These features make Llama-agents a versatile tool for creating anything from complex question-answering systems to collaborative AI assistants and distributed AI workflows. Whether you're just starting out or scaling up to production, Llama-agents has the tools you need to bring your AI ideas to life.


Source documents:
URL: https://www.llamaindex.ai/blog/introducing-llama-agents-a-powerful-framework-for-building-production-multi-agent-ai-systems - Chunk_id: 1
URL: https://www.llamaindex.ai/blog/introducing-llama-agents-a-powerful-framework-for-building-production-multi-agent-ai-systems - Chunk_id: 33
URL: https://www.llamaindex.ai/blog/how-to-build-llm-agents-in-typescript-with-llamaindex-ts-a88ed364a7aa - Chunk_id: 21
URL: https://www.llamaindex.ai/blog/llamaindex-newsletter-2024-04-23 - Chunk_id: 0
URL: https://www.llamaindex.ai/blog/building-better-tools-for-llm-agents-f8c5a6714f11 - Chunk_id: 1
```
Question 2

```
Question: What are the two critical areas of RAG system performance that are assessed in the "Evaluating RAG with LlamaIndex" section of the OpenAI Cookbook?

Thinking...

The "Evaluating RAG with LlamaIndex" section of the OpenAI Cookbook focuses on assessing the performance of RAG (Retrieval-Augmented Generation) systems in two critical areas: the retrieval system and response generation. This means the evaluation looks at how well the system retrieves relevant information and how effectively it generates responses based on that information. The cookbook uses a unique synthetic dataset generation method, called "generate_question_context_pairs," to conduct thorough evaluations in these areas. This helps ensure that the RAG systems developed using LlamaIndex are both effective and efficient.


Source documents:
URL: https://www.llamaindex.ai/blog/openai-cookbook-evaluating-rag-systems-fe393c61fb93 - Chunk_id: 1
URL: https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b - Chunk_id: 42
URL: https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b - Chunk_id: 41
URL: https://www.llamaindex.ai/blog/openai-cookbook-evaluating-rag-systems-fe393c61fb93 - Chunk_id: 0
URL: https://www.llamaindex.ai/blog/llamaindex-newsletter-2023-10-17-33514cbc04a2 - Chunk_id: 5
```

Question 3

```
Question: What are the two main metrics used to evaluate the performance of the different rerankers in the RAG system?

Thinking...

The two main metrics used to evaluate the performance of different rerankers in the RAG system are hit rate and mean reciprocal rank (MRR). These metrics help assess how well the system retrieves relevant information in response to user queries. The hit rate measures the percentage of times the correct answer is found within the top results, while MRR evaluates the rank of the first relevant document, providing a more nuanced view of the system's performance.


Source documents:
URL: https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b - Chunk_id: 42
URL: https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b - Chunk_id: 41
URL: https://www.llamaindex.ai/blog/llamaindex-enhancing-retrieval-performance-with-alpha-tuning-in-hybrid-search-in-rag-135d0c9b8a00 - Chunk_id: 39
URL: https://www.llamaindex.ai/blog/llamaindex-enhancing-retrieval-performance-with-alpha-tuning-in-hybrid-search-in-rag-135d0c9b8a00 - Chunk_id: 40
URL: https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5 - Chunk_id: 32
```