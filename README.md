# Traditional RAG system design

### Pipelines
**\*** Data Ingestion Pipeline
**\*** Embedding + Chunking
**\*** User Query + Prompt
**\*** Retreival Pipeline

## 1. Data Ingestion Pipeline

### 1-1. Document Structure
**\*** pdf, excel, html...
**\*** Parsing -> Document structure (via loaders)

```python
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
```python
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
![image](https://hackmd.io/_uploads/H10gJNWFWx.png)
The files above are default files to feed into the RAG pipeline, it can be swapped out for other PDF, TXT or XLSX files.


### 1-4. Results Running Data_Ingestion_Pipeline.py
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
```python
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
```python
def embed_chunks(self, chunks: List[Any]) -> List[Any]:

        texts = [chunk.page_content for chunk in chunks]  # Removed the meta data from all the document object (only kept the page content)
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Embeddings shape: {embeddings.shape}")  # returns (x, y), x= amount of chunks, y= the dimension of each chunk
        return embeddings
```
As mentioned in the code above, it removes all metadata drom each chunk, only using the page_content. Then uses the "all-MiniLM-L6-v2" embedding model from *HuggingFace* to embed the page_content (in texts). 
### 2-3. Results Running Embedding_Pipeline.py
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

## 3. Vector Storage
### 3-1. ChromaDB Collection
In this RAG pipeline, after all vectors have been successfully chunked, it is then stored in ChromaDB's collection to better control its flow.
```python
def __init__(self):

        self.chromaDB_client = chromadb.Client(Settings(persist_directory="./chroma_db"))  # Where the data base is, will still exist in this file after code executes

        # Deleting a collection without it existing causes error, hence the try/except
        try:
            self.chromaDB_client.delete_collection("the_collection")  # Deletes the collection created from the previous run (in ./chroma_db)
            print("Previous collection deleted. Creating a new one...")
        except Exception:
            print("No existing collection found. Creating a new one...")

        self.collection = self.chromaDB_client.get_or_create_collection(name= "the_collection")

        print("ChromeDB collection created.")
```
What is added to the collection is as followed:
**\*** **IDs:** to keep track of each chunk's source and global index
**\*** **Documents:** the page_content of each chunk
**\*** **Metadatas:** the entirety of each chunk's metadata
**\*** **Embeddings:** the vector values]
```python
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
```
### 3-2. Query
This function will take the user's query' embeddings, calculate the closest value embedding from the entire collection, and returns the top result and its attributes in the form of a dictionary.
```python
# Return type's format
top_docs = {

    "id": results["ids"][0],
    "documents": results["documents"][0],
    "metadatas": results["metadatas"][0],
    "distances": results["distances"][0]

}
    
return top_docs
```
### 3-3. Results Running Vector_Storing.py
Results:
```
...
No existing collection found. Creating a new one...
ChromeDB collection created.
Added (139, 384) size embeddings and its properties into ChromaDB
Completed adding vectors into DB
```
## 4. Main Function: User Query
### 4-1. Structure
**\*** Call the *llama3.1* model
**\*** Pass in a final prompt in the form that includes:

:::info
1. User Query *(ipnut_text)*: The question the user has in regards of the files.
2. System Prompt *(system_promp)*: Deafault rules the LLM must follow 
3. Context *(context_clue)*: By comparing the user's query's embedding with the DB, the context would be the *page_content* of the most similar chunk.
::: 

```python
final_prompt = f"""
        System: {system_prompt}
        User Query: {input_text}
        Context: {context_clue}
"""
```
The final prompt would be entirely passed into the LLM.
### 4-2. Results of running the entire pipeline
File passed in:
![image](https://hackmd.io/_uploads/HyWql-7FZx.png)
Results:
```
...
Added (139, 384) size embeddings and its properties into ChromaDB
>>> Can you show me how to solve the first question of the linear algebra final?
ANSWER: 
To solve the first question, I need to look at Part I, which starts with question 1.

The question is: "Show that if A is a symmetric nonsingular matrix, then A^−1 is also symmetric."

This is an algebraic proof problem, and it appears we can approach it by leveraging properties of symmetric matrices. Specifically, since A is both symmetric and nonsingular (invertible), this should lead us to the conclusion that its inverse A^-1 will share similar characteristics.

To prove it's symmetric:

- We begin with the definition of a symmetric matrix: A = A^T.
- Since A is nonsingular, we know its inverse exists. This implies the existence of A^-1.
- Recall that for any square matrices X and Y, if XY = I (where I is the identity matrix), then YX also equals I (since matrix multiplication is not commutative in general but does hold when dealing with inverses).
- We can manipulate this definition to show that A^-1 * A = A * A^-1 = I
- Because A is symmetric, we know A^T * A = A * A^T. If we replace each instance of A with its transpose (A^T) and multiply both sides by the inverse, then we arrive at the result that the product of A^-1 and itself yields the identity matrix when multiplied together in reverse order.

This reasoning should lead us to conclude that if A is a symmetric nonsingular matrix, its inverse will be symmetric as well.
```
