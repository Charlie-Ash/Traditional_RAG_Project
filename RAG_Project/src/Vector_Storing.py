from typing import List, Any
import chromadb
from chromadb.config import Settings
import numpy as np
from Data_Ingestion_Pipeline import find_all_files
from Embedding_Pipeline import EmbeddingPipeline

# To store: vectors + page contents + other metadata
class VectorStorage:
    
    def __init__(self):

        # Where the data base is, will still exist in this file after code executes
        self.chromaDB_client = chromadb.Client(Settings(persist_directory="./chroma_db", is_persistent= True))  

        # Deleting a collection without it existing causes error, hence the try/except
        try:
            self.chromaDB_client.delete_collection("the_collection")  # Deletes the collection created from the previous run (in ./chroma_db)
            print("Previous collection deleted. Creating a new one...")
        except Exception:
            print("No existing collection found. Creating a new one...")

        self.collection = self.chromaDB_client.get_or_create_collection(name= "the_collection")

        print("ChromeDB collection created.")

    def add_vector(self, chunks: List[Any], embeddings: np.ndarray):

        if len(chunks) != embeddings.shape[0]:  # Quick check
            raise ValueError("Chunks and Embeddings exist mismatch.")

        chunk_ids = [f"chunk_{chunk.metadata.get('chunk_index')}_from_{chunk.metadata.get('source')}" for chunk in chunks]  # Using the chunk's ID and source as the ID stored in the DB (both from the metadata)
        documents = [chunk.page_content for chunk in chunks]  # Page contents as the documents stored in the DB
        metadatas = [chunk.metadata for chunk in chunks]  # Full metadata

        self.collection.add(
            ids= chunk_ids,
            embeddings= embeddings,
            documents= documents,
            metadatas= metadatas
        )

        print(f"Added {embeddings.shape} size embeddings and its properties into ChromaDB")

    def query(self, query_embeddings: np.ndarray, top_results_count: int = 3):

        ''' chroma's return form: (in "results", chroma's nested dictionary format)
        {
            "ids": [["chunk_3_from_animals.pdf"]],
            "documents": [["Cats are mammals..."]],
            "metadatas": [[{"source": "animals.pdf", "chunk_index": 3}]],
            "distances": [[0.12]]
        }
        '''
        
        results = self.collection.query(  # the IDs
            query_embeddings= [query_embeddings.tolist()],
            n_results= top_results_count
        )

        top_docs = {

            "id": results["ids"][0],
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0]

        }

        return top_docs
    

# Test use
if __name__ == "__main__":

    docs = find_all_files("data")
    embed_pipe = EmbeddingPipeline()
    chunks = embed_pipe.chunk_docs(docs)
    embedding = embed_pipe.embed_chunks(chunks)

    vector_DB = VectorStorage()
    vector_DB.add_vector(chunks, embedding)

    print("Completed adding vectors into DB.")