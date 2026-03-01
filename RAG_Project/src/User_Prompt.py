'''
FULL PIPELINE RAN FROM HERE
'''
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from Data_Ingestion_Pipeline import find_all_files
from Embedding_Pipeline import EmbeddingPipeline
from Vector_Storing import VectorStorage

'''
Part 1: Embed data provided for the RAG
'''
# Retreival and Chunking
docs = find_all_files("data")
embed_pipe = EmbeddingPipeline()
chunks = embed_pipe.chunk_docs(docs)
embedding = embed_pipe.embed_chunks(chunks)

# Vector storage in ChromaDB collection
vector_db = VectorStorage()
vector_db.add_vector(chunks, embedding)

'''
Part 2: User query and prompt embedding
'''
llm_name = str("llama3.1")  # LLM model name, change this if a different model is ran
llm = OllamaLLM(model= llm_name)  # Initializing LLM
system_prompt = "Answer with the provided material as context. If the provided context does not contain enough information, please state that you don't know."

input_text = input(">>> ")
while input_text.lower() != "bye":

    # Encoding the query text directly through SentenceTransformer()
    query_embedding = embed_pipe.model.encode(input_text)

    # Vector comparison between "data"'s chunks and the user's query
    top_result = vector_db.query(query_embedding)
    context_clue = top_result.get("documents")

    # Final prompt and LLM invoking
    final_prompt = f"""

        System: {system_prompt}

        User Query: {input_text}

        Context: {context_clue}

    """
    response = llm.invoke(final_prompt)
    print("ANSWER: ")
    print(response)

    # New question
    input_text = input(">>> ")
