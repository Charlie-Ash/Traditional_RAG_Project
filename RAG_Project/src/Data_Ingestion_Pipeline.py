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