from typing import List, Any
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer  # For embedding (with embedding model)
import numpy as np
from Data_Ingestion_Pipeline import find_all_files

class EmbeddingPipeline:

    def __init__(self, embedding_model_name: str =  "all-MiniLM-L6-v2", chunk_size: int = 400, chunk_overlap: int = 80):  # Constructor
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = SentenceTransformer(embedding_model_name)
        print(f"[INFO] Loaded embedding model: {embedding_model_name}")
    
    def chunk_docs(self, documents: List[Any]) -> List[Any]:  # "documents" is a list with the pre-created DOCUMENT data structure

        splitter = RecursiveCharacterTextSplitter(  # Default Separators: ["\n\n", "\n", " ", ""]

            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len

        )

        chunks = splitter.split_documents(documents)  # "chunks" is still a list with DOCUMENT data structure, but now formatted
        print(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks

    def embed_chunks(self, chunks: List[Any]) -> List[Any]:

        texts = [chunk.page_content for chunk in chunks]  # Removed the meta data from all the document object (only kept the page content)
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Embeddings shape: {embeddings.shape}")  # returns (x, y), x= amount of chunks, y= the dimension of each chunk
        return embeddings
    

# Test use
if __name__ == "__main__":

    docs = find_all_files("data")
    embed_pipe = EmbeddingPipeline()
    chunks = embed_pipe.chunk_docs(docs)
    embedding = embed_pipe.embed_chunks(chunks)

    print(f"Example Embeddings: {embedding[0]}")
