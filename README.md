# 🎓 NIT Jalandhar AI Admission Assistant

A **Retrieval-Augmented Generation (RAG) based AI chatbot** designed to answer student queries related to NIT Jalandhar admissions, fees, hostels, courses, eligibility, documents, counselling, and other college-related information.

The system retrieves relevant information from official college documents and uses **NVIDIA AI models** to generate context-grounded answers.

## 🚀 Live Demo

🔗 **[Try the NIT Jalandhar AI Assistant](https://apperchatbot-rtpuejk22hjflwqrrrozis.streamlit.app/)**

---

## 📌 Project Overview

Students often need to search through multiple college documents to find information about admissions, fees, hostel allocation, eligibility, reporting instructions, and other procedures.

This project provides a conversational AI interface where students can ask questions in natural language and receive answers based on the available college documents.

The system follows a complete RAG pipeline:

```text
Student Question
       ↓
Query Expansion
       ↓
Hybrid Retrieval
       ↓
Vector Search + BM25
       ↓
Reciprocal Rank Fusion
       ↓
Relevant Document Chunks
       ↓
NVIDIA Nemotron LLM
       ↓
Context-Grounded Answer
       ↓
Streamlit Chat Interface
