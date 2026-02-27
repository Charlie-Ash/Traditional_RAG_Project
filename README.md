# Traditional RAG system design

### Pipelines
**\*** Data Ingestion Pipeline
**\*** User Query + Prompt
**\*** Retreival Pipeline

## 1. Data Ingestion Pipeline

### 1-1. Document Structure
**\*** pdf, excel, html...
**\*** Parsing -> Document structure (via loaders)

```python=
# LangChain Document Data structure
from langchain_core.documents import Document

doc=Document(
    page_content="this is the main text content I am using to create RAG",
    metadata={
        "source":"exmaple.txt", 
        "pages":1,
        "author":"Charlie Ash",
        "timestamp":"2026-02-06"
    }
)

```
***Page Content***: The main information to be embedded and searched (must be a string)
***Meta Data***: Additional info

### 1-2. Directory Loader Structure
**\*** Assists with loading many files in the directory
```python=
# Directory Loader
from langchain_community.document_loaders import DirectoryLoader

# Load all the text files from the directory
dir_loader=DirectoryLoader(
    "../data/text_files",
    glob="**/*.txt", # Pattern to match files  
    loader_cls= TextLoader, # Loader class to use
    loader_kwargs={'encoding': 'utf-8'},
    show_progress=False
)

documents=dir_loader.load()
```
(*"documents"* will return a list of ***Document*** structures of all the specified files in the directory)

### 1-3. Data File
![image](https://hackmd.io/_uploads/SyMxsMvP-l.png)


### 1-4. Data Ingestion Full Pipeline
```python=
from pathlib import Path
from typing import List, Any
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader

def find_all_files(directory : str) -> List[Any]:  # Assumes the directory is right under the project file

    # Uses project's "data" file
    BASE_DIR = Path(__file__).resolve()
    SOURCE_DIR = BASE_DIR.parent
    PROJECT_DIR = SOURCE_DIR.parent
    data_path = PROJECT_DIR / directory  # Path-joining
    print(f"Data Path: {data_path}")
    documents = []

    # PDF files
    pdf_files = list(data_path.glob("**/*.pdf"))  #  Any file after data that is "pdf"
    print(f"Found {len(pdf_files)} PDF files: {[str(f) for f in pdf_files]}")

    file_counter = 0
    for pdf_file in pdf_files:  # Load all PDF files

        print(f"Loading PDF file[{file_counter}]: {pdf_file}")

        try:

            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load() # List of "Documents" datatype (it's a list since the loader often times splits the file into chunks on its own)
            print(f"Loaded {len(loaded)} PDF docs from {pdf_file}")
            
            for doc in loaded:  # Adding metadatas to the DOCUMENT data structure

                doc.metadata["source"] = pdf_file.name()
                doc.metadata["path"] = str(pdf_file.absolute())

            documents.extend(loaded)

        except Exception as e:
            print(f"[ERROR] Error loading {pdf_file} PDF file: {e.with_traceback()}")

        file_counter = file_counter + 1

    # Excel files
    xlsx_files = list(data_path.glob("**/*.xlsx"))  #  Any file after data that is "pdf"
    print(f"Found {len(xlsx_files)} Excel files: {[str(f) for f in xlsx_files]}")

    file_counter = 0
    for xlsx_file in xlsx_files:  # Load all Excel files

        print(f"Loading Excel file[{file_counter}]: {xlsx_file}")

        try:

            loader = UnstructuredExcelLoader(str(xlsx_file))
            loaded = loader.load() # List of "Documents" datatype
            print(f"Loaded {len(loaded)} Excel docs from {xlsx_file}")

            for doc in loaded:  # Adding metadatas to the DOCUMENT data structure

                doc.metadata["source"] = xlsx_file.name()
                doc.metadata["path"] = str(xlsx_file.absolute())

            documents.extend(loaded)

        except Exception as e:
            print(f"[ERROR] Error loading {xlsx_file} Excel file: {e.with_traceback()}")

        file_counter = file_counter + 1

    # Txt files
    txt_files = list(data_path.glob("**/*.txt"))  #  Any file after data that is "pdf"
    print(f"Found {len(txt_files)} Txt files: {[str(f) for f in txt_files]}")

    file_counter = 0
    for txt_file in txt_files:  # Load all Excel files
        
        print(f"Loading Txt file[{file_counter}]: {txt_file}")

        try:

            loader = TextLoader(str(txt_file))
            loaded = loader.load() # List of "Documents" datatype
            print(f"Loaded {len(loaded)} Txt docs from {txt_file}")
            documents.extend(loaded)

            for doc in loaded:  # Adding metadatas to the DOCUMENT data structure

                doc.metadata["source"] = txt_file.name()
                doc.metadata["path"] = str(txt_file.absolute())

            documents.extend(loaded)

        except Exception as e:
            print(f"[ERROR] Error loading {txt_file} Txt file: {e.with_traceback()}")

        file_counter = file_counter + 1

    return documents


# Test usage
if __name__ == "__main__":

    documents = find_all_files("data")
    for f in documents:
        print("File aquired: " + f.metadata["source"])
```
Results:
```
Data Path: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data
Found 4 PDF files: ['C:\\Users\\USER\\PycharmProjects\\Traditional_RAG_Project\\RAG_Project\\data\\au24final.pdf', 'C:\\Users\\USER\\PycharmProjects\\Traditional_RAG_Project\\RAG_Project\\data\\Prob_Stat_final.pdf', 'C:\\Users\\USER\\PycharmProjects\\Traditional_RAG_Project\\RAG_Project\\data\\Project_Presentation_Rules.pdf', 'C:\\Users\\USER\\PycharmProjects\\Traditional_RAG_Project\\RAG_Project\\data\\Testing_Order_Time.pdf']
Loading PDF file[0]: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\au24final.pdf
Ignoring wrong pointing object 6 0 (offset 0)
Ignoring wrong pointing object 8 0 (offset 0)
Ignoring wrong pointing object 10 0 (offset 0)
Ignoring wrong pointing object 12 0 (offset 0)
Ignoring wrong pointing object 14 0 (offset 0)
Ignoring wrong pointing object 16 0 (offset 0)
Ignoring wrong pointing object 18 0 (offset 0)
Ignoring wrong pointing object 20 0 (offset 0)
Ignoring wrong pointing object 22 0 (offset 0)
Loaded 2 PDF docs from C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\au24final.pdf
Loading PDF file[1]: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
Loaded 11 PDF docs from C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
Loading PDF file[2]: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Project_Presentation_Rules.pdf
Loaded 1 PDF docs from C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Project_Presentation_Rules.pdf
Loading PDF file[3]: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Testing_Order_Time.pdf
Loaded 1 PDF docs from C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Testing_Order_Time.pdf
Found 0 Excel files: []
Found 2 Txt files: ['C:\\Users\\USER\\PycharmProjects\\Traditional_RAG_Project\\RAG_Project\\data\\countries.txt', 'C:\\Users\\USER\\PycharmProjects\\Traditional_RAG_Project\\RAG_Project\\data\\gibberish.txt']
Loading Txt file[0]: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\countries.txt
Loaded 1 Txt docs from C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\countries.txt
Loading Txt file[1]: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\gibberish.txt
Loaded 1 Txt docs from C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\gibberish.txt
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\au24final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\au24final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Prob_Stat_final.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Project_Presentation_Rules.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\Testing_Order_Time.pdf
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\countries.txt
File aquired: C:\Users\USER\PycharmProjects\Traditional_RAG_Project\RAG_Project\data\gibberish.txt

Process finished with exit code 0

```

## 2. Chunking & Embedding
**\*** After parsing, we get each chunk, and embed them.
**\*** Create **EmbeddingPipeline** class 
**\*** Initialize the class with chunk size of 1000, overlap of 200
**\*** Switched from the *Ollama* to the *HuggingFace* embedding model. The embedding will provide more stability, and renders me to use **SentenceTransformer** to chunck data

### 2-1. Chunk Documents
```python=
def chunk_docs(self, documents: List[Any]) -> List[Any]: # "documents" is a list with the pre-created DOCUMENT data structure


        splitter = RecursiveCharacterTextSplitter(  # Default Separators: ["\n\n", "\n", " ", ""]

            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len

        )

        chunks = splitter.split_documents(documents)  # "chunks" is still a list with DOCUMENT data structure, but now formatted
        print(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks
```
The function's  main goal is to split infomation into chunks, which are all small peices of **Document** data structure.
### 2-2. Embed Documents
```python=
def embed_chunks(self, chunks: List[Any]) -> List[Any]:

        texts = [chunk.page_content for chunk in chunks]  # Removed the meta data from all the document object (only kept the page content)
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Embeddings shape: {embeddings.shape}")  # returns (x, y), x= amount of chunks, y= the dimension of each chunk
        return embeddings
```
As mentioned in the code above, it removes all metadata drom each chunk, only using the page_content. Then uses the "all-MiniLM-L6-v2" embedding model from *HuggingFace* to embed the page_content (in texts). 
### 2-3. Embedding Full Pipeline
```python=
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
    
    def chunk_docs(self, documents: List[Any]) -> List[Any]:

        '''
        "documents" is a list of list of the pre-created DOCUMENT data structure (double list)
        The amount of items in "documents" is the amount of files in the "data" folder
        Each item representing a file, an each item (a list) will have different amounts of chunks, depending on the loader during data ingestion.
        '''

        splitter = RecursiveCharacterTextSplitter(  # Default Separators: ["\n\n", "\n", " ", ""]

            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len

        )

        chunks = []  # "chunks" is still a list with DOCUMENT data structure, but now formatted

        for doc in documents:

            splitted_chunks = splitter.split_documents([doc])

            for i, chunk in splitted_chunks:  # Adding metadata for each chunk

                chunk.metadata["chunk_index"] = i
                chunk.metadata["source"] = doc.metadata.get("source")
                chunk.metadata["path"] = doc.metadata.get("path")

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

```
Results:
```
......
Loading weights: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 4460.04it/s, Materializing param=pooler.dense.weight]
BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2
Key                     | Status     | Details
------------------------+------------+--------
embeddings.position_ids | UNEXPECTED |

Notes:
- UNEXPECTED    :can be ignored when loading from different task/architecture; not ok if you expect identical arch.
[INFO] Loaded embedding model: all-MiniLM-L6-v2
Split 17 documents into 19 chunks
Generating embeddings for 19 chunks...
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.51it/s] 
Embeddings shape: (19, 384)
Example Embeddings: [-9.21084452e-03  3.88275571e-02  1.27735343e-02 -5.38459495e-02
 -2.59408783e-02 -2.79497635e-03  7.48210549e-02 -1.00793473e-01
 -7.93170109e-02  5.27221486e-02  4.84477989e-02  5.39705949e-03
  2.26148274e-02  5.38197905e-03 -4.94310260e-02  2.14767810e-02
 -3.61346751e-02 -6.90350309e-02  9.81367007e-03  2.19894852e-02
 -9.25365239e-02 -7.82115012e-02 -5.28241880e-02  5.94564993e-03
  6.89272881e-02  9.67862830e-03  6.23044111e-02  8.13840609e-03
 -4.73254248e-02 -2.40997644e-03 -3.54671143e-02  9.45523009e-03
  3.67199704e-02  4.50931937e-02 -4.45392840e-02 -7.56235272e-02
  7.12287351e-02  4.60161008e-02  4.83624525e-02  7.07196146e-02
  4.19389270e-02 -1.15083210e-01  1.83928553e-02 -7.72474520e-03
  3.79715152e-02 -5.10256737e-02 -1.84535142e-02 -1.17989473e-01
  5.63323423e-02 -4.90062572e-02 -7.73869157e-02  6.55942857e-02
 -1.49976894e-01 -3.32234018e-02 -1.11858398e-01 -9.60983634e-02
 ......
```