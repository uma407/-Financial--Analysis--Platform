"""
Vector store utilities for embeddings and retrieval.
Supports ChromaDB and FAISS as configured in config.py
"""
from __future__ import annotations

import os
from typing import List, Dict

from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain_community.vectorstores import Chroma

from config import (
    EMBEDDING_MODEL,
    VECTOR_STORE_TYPE,
    CHROMA_PERSIST_DIR,
    FAISS_INDEX_PATH,
)


def get_embedding_model():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)


class VectorStore:
    def __init__(self, store_type: str = VECTOR_STORE_TYPE):
        self.store_type = store_type
        self.embedding_model = get_embedding_model()
        self.store = None

    def _as_documents(self, items: List[Dict[str, str]]) -> List[Document]:
        docs = []
        for item in items:
            docs.append(
                Document(
                    page_content=item["text"],
                    metadata={
                        "id": item.get("id"),
                        "source_id": item.get("source_id"),
                    },
                )
            )
        return docs

    def load_or_create(self, items: List[Dict[str, str]]) -> None:
        """Load a persisted store if present, otherwise create from items."""
        docs = self._as_documents(items)
        if self.store_type == "chroma":
            os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
            self.store = Chroma.from_documents(
                documents=docs,
                embedding=self.embedding_model,
                persist_directory=CHROMA_PERSIST_DIR,
            )
        else:
            if os.path.exists(FAISS_INDEX_PATH):
                self.store = FAISS.load_local(
                    FAISS_INDEX_PATH,
                    embeddings=self.embedding_model,
                    allow_dangerous_deserialization=True,
                )
            else:
                self.store = FAISS.from_documents(documents=docs, embedding=self.embedding_model)
                self.store.save_local(FAISS_INDEX_PATH)

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        if not self.store:
            raise ValueError("Vector store is not initialized. Call load_or_create first.")
        return self.store.similarity_search(query, k=k)
