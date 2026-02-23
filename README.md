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
            loaded = loader.load() # List of "Documents" datatype
            print(f"Loaded {len(loaded)} PDF docs from {pdf_file}")
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
As mentioned in the code above, it removes all metadata drom each chunk, only using the page_content. Then uses the "all-MiniLM-L6-v2" model to embed the page_content (in texts). 
### 2-3. Embedding Full Pipeline
```python=
from typing import List, Any
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer  # For embedding
import numpy as np
from Data_Ingestion_Pipeline import find_all_files

class EmbeddingPipeline:

    def __init__(self, model_name: str =  "all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 200):  # Constructor
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = SentenceTransformer(model_name)
        print(f"[INFO] Loaded embedding model: {model_name}")
    
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
```
Results:
```
......
Loading weights: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 5015.60it/s, Materializing param=pooler.dense.weight]
BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2
Key                     | Status     | Details
------------------------+------------+--------
embeddings.position_ids | UNEXPECTED |

Notes:
- UNEXPECTED    :can be ignored when loading from different task/architecture; not ok if you expect identical arch.
[INFO] Loaded embedding model: all-MiniLM-L6-v2
Split 17 documents into 10 chunks
Generating embeddings for 10 chunks...
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.97it/s] 
Embeddings shape: (10, 384)
Example Embeddings: [ 2.18977518e-02 -8.19026551e-04  3.43371677e-04 -7.95536712e-02
 -1.38868801e-02  9.04212892e-03  5.48933372e-02 -1.41972706e-01
 -3.19621898e-02  5.25665767e-02  4.99323159e-02 -3.26099172e-02
  5.73712364e-02 -2.18379889e-02 -1.14194555e-02  1.94990337e-02
 -2.95626856e-02 -4.42739613e-02  9.88000166e-03  3.45877074e-02
 -4.88435142e-02 -1.05402507e-01 -5.75334765e-02 -2.14974135e-02
  5.55228889e-02  3.09163742e-02  6.40546009e-02  1.38973659e-02
 -2.47491784e-02  7.98171503e-04 -5.78473061e-02  9.43608209e-03
 -1.49547476e-02  5.45878671e-02 -1.01921307e-02 -8.89268816e-02
  2.27785092e-02  2.74050161e-02  7.51130795e-03  1.12575971e-01
  1.65363643e-02 -1.24522060e-01  5.16394852e-03 -1.62559580e-02
  2.42964067e-02 -2.35713869e-02 -2.55828574e-02 -1.03695765e-01
  1.51742343e-02 -8.13494176e-02 -5.16008958e-02  5.00273146e-02
 -8.98541659e-02 -4.57129925e-02 -1.14585407e-01 -1.19463436e-01
 ......
```