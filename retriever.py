from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from config import (
    NVIDIA_API_KEY,
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL
)


# =========================================================
# NVIDIA EMBEDDINGS
# =========================================================

embeddings = NVIDIAEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=NVIDIA_API_KEY
)


# =========================================================
# LOAD CHROMA DATABASE
# =========================================================

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)


# =========================================================
# LOAD ALL DOCUMENTS FROM CHROMA
# =========================================================

data = vectorstore.get(
    include=["documents", "metadatas"]
)

all_documents = []

for content, metadata in zip(
    data["documents"],
    data["metadatas"]
):

    all_documents.append(
        Document(
            page_content=content,
            metadata=metadata or {}
        )
    )


print(f"Loaded {len(all_documents)} document chunks for BM25.")


# =========================================================
# CREATE BM25 INDEX
# =========================================================

tokenized_documents = [
    doc.page_content.lower().split()
    for doc in all_documents
]

bm25 = BM25Okapi(tokenized_documents)


# =========================================================
# HYBRID SEARCH
# =========================================================

def hybrid_search(
    query,
    vector_k=8,
    bm25_k=8,
    final_k=5
):

    # -----------------------------------------------------
    # VECTOR SEARCH
    # -----------------------------------------------------

    vector_results = vectorstore.similarity_search(
        query,
        k=vector_k
    )


    # -----------------------------------------------------
    # BM25 KEYWORD SEARCH
    # -----------------------------------------------------

    tokenized_query = query.lower().split()

    bm25_scores = bm25.get_scores(
        tokenized_query
    )


    ranked_bm25_indices = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )[:bm25_k]


    bm25_results = [
        all_documents[i]
        for i in ranked_bm25_indices
    ]


    # -----------------------------------------------------
    # RECIPROCAL RANK FUSION
    # -----------------------------------------------------

    scores = {}
    documents = {}


    # Vector results
    for rank, doc in enumerate(vector_results):

        key = doc.page_content

        documents[key] = doc

        scores[key] = scores.get(key, 0) + (
            1 / (60 + rank + 1)
        )


    # BM25 results
    for rank, doc in enumerate(bm25_results):

        key = doc.page_content

        documents[key] = doc

        scores[key] = scores.get(key, 0) + (
            1 / (60 + rank + 1)
        )


    # -----------------------------------------------------
    # SORT RESULTS
    # -----------------------------------------------------

    ranked_documents = sorted(
        documents.values(),
        key=lambda doc: scores[doc.page_content],
        reverse=True
    )


    return ranked_documents[:final_k]