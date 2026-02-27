from typing import List, Any
import chromadb
from chromadb.config import Settings
import numpy as np

# To store: vectors + text + metadata
class VectorStorage:
    
    def __init__(self):

        self.chromaDB_client = chromadb.Client(Settings(persist_directory="./chroma_db"))  # Where the data base is, will still exist in this file after code executes
        self.chromaDB_client.delete_collection("the_collection")  # Deletes the collection created from the previous run (in ./chroma_db)
        self.collection = self.chromaDB_client.get_or_create_collection(name= "the_collection")

    def add_vector(self, chunks: List[Any], embeddings: np.ndarray):
        pass
        