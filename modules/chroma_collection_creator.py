import streamlit as st
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class ChromaCollectionCreator:
    def __init__(self, processor, embed_model):
        """
        Initializes the ChromaCollectionCreator with a DocumentProcessor instance and embeddings configuration.
        :param processor: An instance of DocumentProcessor that has processed documents.
        :param embeddings_config: An embedding client for embedding documents.
        """
        self.processor = processor   
        self.embed_model = embed_model
        self.db = None                  # This will hold the Chroma collection
    
    def create_chroma_collection(self):
        """
        Create a Chroma collection from the documents processed by the DocumentProcessor instance
        """
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon="🚨")
            return

        # Split documents into text chunks
        text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                )
        
        texts = text_splitter.split_documents(self.processor.pages)

        if texts is not None:
            st.success(f"Successfully split pages to {len(texts)} documents!", icon="✅")

        # Create the Chroma Collection    
        try: 
            self.db = Chroma.from_documents(
                documents=texts,
                embedding=self.embed_model
            )
            st.success("Successfully created Chroma Collection!", icon="✅")
        except Exception as e:
             st.error("Failed to create Chroma Collection!", icon="🚨")           
    
    def query_chroma_collection(self, query) -> Document:
        """
        Queries the created Chroma collection for documents similar to the query.
        :param query: The query string to search for in the Chroma collection.
        
        Returns the first matching document from the collection with similarity score.
        """
        if self.db:
            docs = self.db.similarity_search_with_relevance_scores(query)
            if docs:
                return docs[0]
            else:
                st.error("No matching documents found!", icon="🚨")
        else:
            st.error("Chroma Collection has not been created!", icon="🚨")