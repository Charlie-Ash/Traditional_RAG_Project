import chromadb

# To store: vectors + text + metadata
class VectorStorage:
    
    def __init__(self):

        chromaDB_client = chromadb.Client()
        collection = chromaDB_client.create_collection("TheCollection")
        