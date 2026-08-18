from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.chat_history import InMemoryChatMessageHistory

from config import NVIDIA_API_KEY, LLM_MODEL
from retriever import hybrid_search


# =========================================================
# NVIDIA LLM
# =========================================================

llm = ChatNVIDIA(
    model=LLM_MODEL,
    api_key=NVIDIA_API_KEY,
    temperature=0.2
)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are a helpful admission assistant for NIT Jalandhar.

Your job is to answer questions from students who are seeking
information about the college.

Use ONLY the information provided in the context.

If the answer is not available in the context, say:

"I couldn't find this information in the available college documents."

Do not make up information.

Give clear, concise and student-friendly answers.



You also have access to the previous conversation.
Use the conversation history to understand follow-up questions.

However, do not use information from conversation history as
factual college information unless it is also supported by the
provided context.
"""


# =========================================================
# CONVERSATION MEMORY
# =========================================================

chat_history = InMemoryChatMessageHistory()


# =========================================================
# QUERY EXPANSION
# =========================================================

def generate_search_queries(question):

    prompt = f"""
You are a search query generator for a college information
retrieval system.

The student's question may be vague or use different wording
from the college documents.

Generate 3 alternative search queries that could help retrieve
the correct information from college PDF documents.

Rules:

1. Keep the original meaning.
2. Use important keywords.
3. Use alternative wording where useful.
4. Include abbreviations when relevant.
5. Do NOT answer the question.
6. Do NOT invent facts or names that are not present in the
   student's question.
7. Return ONLY the search queries.
8. Put one query on each line.

Student question:
{question}
"""

    response = llm.invoke(prompt)

    text = response.content

    # Make sure response is treated as text
    if not isinstance(text, str):
        text = str(text)

    queries = []

    for line in text.split("\n"):

        line = line.strip()

        # Remove common numbering
        if line.startswith("1."):
            line = line[2:].strip()

        elif line.startswith("2."):
            line = line[2:].strip()

        elif line.startswith("3."):
            line = line[2:].strip()

        if line:
            queries.append(line)


    # Always keep original question
    # This prevents query expansion from losing
    # the user's original meaning.

    final_queries = [question]

    for query in queries:

        if query.lower() != question.lower():
            final_queries.append(query)


    return final_queries[:4]


# =========================================================
# ASK QUESTION
# =========================================================

def ask_question(question):

    # -----------------------------------------------------
    # STEP 1: GENERATE SEARCH QUERIES
    # -----------------------------------------------------

    search_queries = generate_search_queries(question)


    # print("\nSearch queries:")

    # for query in search_queries:
    #     print("-", query)


    # -----------------------------------------------------
    # STEP 2: HYBRID SEARCH FOR EACH QUERY
    # -----------------------------------------------------

    all_results = []


    for query in search_queries:

        results = hybrid_search(
            query,
            vector_k=8,
            bm25_k=8,
            final_k=5
        )

        all_results.extend(results)


    # -----------------------------------------------------
    # STEP 3: REMOVE DUPLICATE DOCUMENT CHUNKS
    # -----------------------------------------------------

    unique_documents = {}

    for doc in all_results:

        key = doc.page_content

        if key not in unique_documents:

            unique_documents[key] = doc


    documents = list(
        unique_documents.values()
    )


    # Keep a reasonable amount of context
    documents = documents[:8]


    # -----------------------------------------------------
    # STEP 4: CHECK IF DOCUMENTS WERE FOUND
    # -----------------------------------------------------

    if not documents:

        return (
            "I couldn't find relevant information in the "
            "available college documents."
        )


    # -----------------------------------------------------
    # STEP 5: DEBUG - SHOW RETRIEVED DOCUMENTS
    # -----------------------------------------------------

    # print("\n========== RETRIEVED DOCUMENTS ==========")

    # for i, doc in enumerate(documents):

    #     print(f"\n--- RESULT {i + 1} ---")

    #     print(
    #         f"Source: "
    #         f"{doc.metadata.get('source', 'Unknown')}"
    #     )

    #     print(
    #         f"Page: "
    #         f"{doc.metadata.get('page', 'Unknown')}"
    #     )

    #     print(
    #         f"Content:\n"
    #         f"{doc.page_content[:700]}"
    #     )

    # print("\n==========================================\n")


    # -----------------------------------------------------
    # STEP 6: BUILD CONTEXT
    # -----------------------------------------------------

    context = "\n\n".join(
        [
            f"Source: {doc.metadata.get('source', 'Unknown')}\n"
            f"Page: {doc.metadata.get('page', 'Unknown')}\n"
            f"Content:\n{doc.page_content}"
            for doc in documents
        ]
    )


    # -----------------------------------------------------
    # STEP 7: PREVIOUS CONVERSATION
    # -----------------------------------------------------

    history = ""

    for message in chat_history.messages:

        if message.type == "human":

            history += (
                f"Student: {message.content}\n"
            )

        elif message.type == "ai":

            history += (
                f"Chatbot: {message.content}\n"
            )


    # -----------------------------------------------------
    # STEP 8: FINAL LLM PROMPT
    # -----------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

PREVIOUS CONVERSATION:
{history}

CURRENT CONTEXT FROM COLLEGE DOCUMENTS:
{context}

CURRENT STUDENT QUESTION:
{question}

Answer the student's question using the provided context.

If the context contains the answer, answer it directly.

If the context does not contain the answer, say:

"I couldn't find this information in the available college documents."

ANSWER:
"""


    # -----------------------------------------------------
    # STEP 9: CALL NVIDIA LLM
    # -----------------------------------------------------

    response = llm.invoke(prompt)

    answer = response.content


    # -----------------------------------------------------
    # STEP 10: SAVE CONVERSATION
    # -----------------------------------------------------

    chat_history.add_user_message(
        question
    )

    chat_history.add_ai_message(
        answer
    )


    return answer