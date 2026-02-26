import chromadb
from chromadb.config import Settings

# To store: vectors + text + metadata
class VectorStorage:
    
    def __init__(self):

        chromaDB_client = chromadb.Client(Settings(persist_directory="./chroma_db"))  # Where the data base is, will still exist in this file after code executes
        chromaDB_client.delete_collection("the_collection")  # Deletes the collection created from the previous run (in ./chroma_db)
        collection = chromaDB_client.create_collection("the_collection")
        