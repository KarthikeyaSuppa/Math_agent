#kb.py
import os
import glob
import uuid
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DATA_DIR_NAME = "Data"

class MathKnowledgeBase:
    def __init__(self):
        """Initialize the math knowledge base with Pinecone."""
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )
        
        # Initialize Pinecone client and get index instance
        try:
            # Initialize the Pinecone client
            self.pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
            
            # Store the index name
            self.index_name = PINECONE_INDEX_NAME
            
            # Connect to the index
            self.index = self.pc.Index(self.index_name)
            
            # Get stats to verify connection
            stats = self.index.describe_index_stats()
            print(f"Connected to Pinecone index '{self.index_name}' with {stats['total_vector_count']} vectors.")
            
        except Exception as e:
            print(f"Error initializing Pinecone connection: {e}")
            self.index = None
            raise

        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.absolute_data_dir = os.path.join(self.project_root, DATA_DIR_NAME)

    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with data from PDF files in the DATA folder."""
        try:
            pdf_files = glob.glob(os.path.join(self.absolute_data_dir, "*.pdf"))

            if not pdf_files:
                print(f"No PDF files found in {self.absolute_data_dir}. No data to add.")
                return

            all_docs = []
            for pdf_path in pdf_files:
                try:
                    loader = PyPDFLoader(pdf_path)
                    documents = loader.load()
                    
                    for doc in documents:
                        doc.metadata["source"] = os.path.basename(pdf_path)
                        doc.metadata["page"] = doc.metadata.get("page", 0) + 1

                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                        length_function=len,
                        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
                    )
                    chunked_documents = text_splitter.split_documents(documents)
                    all_docs.extend(chunked_documents)
                    print(f"Processed {len(chunked_documents)} chunks from {os.path.basename(pdf_path)}")
                except Exception as load_ex:
                    print(f"Error processing PDF file {pdf_path}: {load_ex}")
            
            if all_docs and self.index:
                print(f"Adding {len(all_docs)} chunks to Pinecone index '{self.index_name}'...")
                self._add_documents_to_pinecone(all_docs)
                print(f"Successfully added documents to Pinecone index '{self.index_name}'.")
            elif not self.index:
                print("Pinecone index is not initialized. Cannot add documents.")

        except Exception as e:
            print(f"Error adding data to knowledge base: {e}")

    def _add_documents_to_pinecone(self, documents, batch_size=100):
        """Add documents to Pinecone in batches."""
        total_batches = (len(documents) + batch_size - 1) // batch_size
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            texts = [doc.page_content for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            
            # Get embeddings
            embeddings = self.embeddings.embed_documents(texts)
            
            # Prepare vectors for upsert
            vectors = []
            for j, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
                # Create a unique ID for each vector
                vector_id = f"doc_{uuid.uuid4()}"
                vectors.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {**metadata, "text": text}
                })
            
            # Upsert to Pinecone
            self.index.upsert(vectors=vectors)
            
            print(f"Added batch {i//batch_size + 1} of {total_batches}")

    def search_knowledge_base(self, query, top_k=3):
        """Search the knowledge base for similar text chunks."""
        if not hasattr(self, 'index') or self.index is None:
            print("Error: Pinecone index not initialized.")
            return []
        
        try:
            # Get the embedding for the query
            query_embedding = self.embeddings.embed_query(query)
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Convert to Document objects with scores
            formatted_results = []
            for match in results.matches:
                doc = Document(
                    page_content=match.metadata.get("text", ""),
                    metadata={k: v for k, v in match.metadata.items() if k != "text"}
                )
                formatted_results.append((doc, match.score))
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching index '{self.index_name}': {e}")
            return []

    def add_to_knowledge_base(self, text_content, metadata=None):
        """Add a new text content (document) to the knowledge base."""
        if not hasattr(self, 'index') or self.index is None:
            print("Error: Pinecone index not initialized.")
            return False, "Pinecone index not initialized."
        
        try:
            if metadata is None:
                metadata = {}
                
            # Get embedding for the text
            embedding = self.embeddings.embed_query(text_content)
            
            # Create a unique ID
            vector_id = f"doc_{uuid.uuid4()}"
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[{
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {**metadata, "text": text_content}
                }]
            )
            
            print(f"Successfully added document to Pinecone index '{self.index_name}'.")
            return True, "Added to knowledge base successfully"
        except Exception as e:
            print(f"Error adding document to knowledge base: {e}")
            return False, f"Error adding to knowledge base: {e}"

if __name__ == "__main__":
    print("Attempting to initialize Math Knowledge Base...")
    try:
        math_kb = MathKnowledgeBase()
        print("MathKnowledgeBase object created.")
        
        # If initialization was successful, attempt to add documents from Data folder
        if hasattr(math_kb, 'index') and math_kb.index:
            print("Vector database initialized, attempting to load data from PDF files...")
            math_kb._initialize_knowledge_base() # Load data if available
        else:
            print("Vector database could not be initialized.")

    except Exception as e:
        print(f"Failed to initialize Math Knowledge Base: {e}")