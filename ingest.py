import os
import io

import pymupdf
import pytesseract

from PIL import Image

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_chroma import Chroma

from config import (
    NVIDIA_API_KEY,
    PDF_FOLDER,
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL
)


# =========================================================
# OCR SETTINGS
# =========================================================

OCR_LANGUAGE = "eng"

# Render PDF pages at higher resolution for better OCR
OCR_ZOOM = 2.5


# =========================================================
# EXTRACT TEXT + OCR FROM PDF
# =========================================================

def extract_pdf_with_ocr(pdf_path):

    print(f"\nProcessing: {pdf_path}")

    pdf = fitz.open(pdf_path)

    documents = []

    for page_number, page in enumerate(pdf):

        print(
            f"  Processing page "
            f"{page_number + 1}/{len(pdf)}..."
        )

        # -------------------------------------------------
        # NORMAL PDF TEXT
        # -------------------------------------------------

        normal_text = page.get_text("text").strip()


        # -------------------------------------------------
        # RENDER PAGE AS IMAGE
        # -------------------------------------------------

        matrix = fitz.Matrix(
            OCR_ZOOM,
            OCR_ZOOM
        )

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        image_bytes = pix.tobytes("png")

        image = Image.open(
            io.BytesIO(image_bytes)
        )


        # -------------------------------------------------
        # OCR
        # -------------------------------------------------

        try:

            ocr_text = pytesseract.image_to_string(
                image,
                lang=OCR_LANGUAGE,
                config="--psm 6"
            ).strip()

        except Exception as e:

            print(
                f"  OCR error on page "
                f"{page_number + 1}: {e}"
            )

            ocr_text = ""


        # -------------------------------------------------
        # COMBINE NORMAL TEXT + OCR TEXT
        # -------------------------------------------------

        if normal_text and ocr_text:

            # Avoid storing OCR if it is essentially
            # the same text already extracted from PDF.
            normal_words = set(
                normal_text.lower().split()
            )

            ocr_words = set(
                ocr_text.lower().split()
            )

            overlap = 0

            if ocr_words:

                overlap = (
                    len(normal_words & ocr_words)
                    / len(ocr_words)
                )


            if overlap > 0.85:

                final_text = normal_text

            else:

                final_text = (
                    normal_text
                    + "\n\n"
                    + "TEXT DETECTED FROM IMAGES:\n"
                    + ocr_text
                )

        elif normal_text:

            final_text = normal_text

        elif ocr_text:

            final_text = (
                "TEXT DETECTED FROM IMAGE:\n"
                + ocr_text
            )

        else:

            final_text = ""


        # -------------------------------------------------
        # SAVE DOCUMENT
        # -------------------------------------------------

        if final_text.strip():

            documents.append(
                Document(
                    page_content=final_text,
                    metadata={
                        "source": os.path.basename(
                            pdf_path
                        ),
                        "page": page_number + 1,
                        "ocr_used": bool(ocr_text)
                    }
                )
            )


    pdf.close()

    return documents


# =========================================================
# LOAD ALL PDFs
# =========================================================

def load_all_pdfs():

    all_documents = []

    if not os.path.exists(PDF_FOLDER):

        print(
            f"ERROR: Folder '{PDF_FOLDER}' "
            f"does not exist."
        )

        return []


    pdf_files = [
        file
        for file in os.listdir(PDF_FOLDER)
        if file.lower().endswith(".pdf")
    ]


    if not pdf_files:

        print(
            f"No PDF files found in "
            f"'{PDF_FOLDER}'."
        )

        return []


    print(
        f"\nFound {len(pdf_files)} PDF files."
    )


    for filename in pdf_files:

        pdf_path = os.path.join(
            PDF_FOLDER,
            filename
        )

        documents = extract_pdf_with_ocr(
            pdf_path
        )

        all_documents.extend(
            documents
        )


    return all_documents


# =========================================================
# CREATE VECTOR DATABASE
# =========================================================

def create_vector_database():

    print("=" * 60)
    print("       NIT JALANDHAR RAG INGESTION")
    print("=" * 60)

    print("\nLoading PDFs with OCR...")

    documents = load_all_pdfs()


    if not documents:

        print(
            "\nNo documents were extracted."
        )

        return


    print(
        f"\nExtracted {len(documents)} pages."
    )


    # =====================================================
    # TEXT CHUNKING
    # =====================================================

    print("\nCreating chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        documents
    )


    print(
        f"Created {len(chunks)} chunks."
    )


    # =====================================================
    # NVIDIA EMBEDDINGS
    # =====================================================

    print("\nCreating NVIDIA embeddings...")

    embeddings = NVIDIAEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=NVIDIA_API_KEY
    )


    # =====================================================
    # DELETE OLD CHROMA DATABASE
    # =====================================================

    if os.path.exists(CHROMA_PATH):

        print(
            "\nWARNING: Existing Chroma database "
            "will be replaced."
        )

        import shutil

        shutil.rmtree(
            CHROMA_PATH
        )


    # =====================================================
    # CREATE CHROMA
    # =====================================================

    print(
        "\nCreating new ChromaDB..."
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH
    )


    print("\n" + "=" * 60)
    print("VECTOR DATABASE CREATED SUCCESSFULLY")
    print("=" * 60)

    print(
        f"\nDatabase location: {CHROMA_PATH}"
    )

    print(
        f"Total pages: {len(documents)}"
    )

    print(
        f"Total chunks: {len(chunks)}"
    )

    print(
        "\nOCR text from images has been "
        "included in the vector database."
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    create_vector_database()