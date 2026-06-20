from pathlib import Path
import json

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = "data/DPM-2025-VOLUME-II.pdf"

def main():

    loader = PyPDFLoader(PDF_PATH)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    output = []

    for idx, chunk in enumerate(chunks):

        output.append({
            "id": idx,
            "text": chunk.page_content,
            "page": chunk.metadata.get("page", -1)
        })

    Path("vectorstore").mkdir(exist_ok=True)

    with open(
        "vectorstore/chunks.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            ensure_ascii=False
        )

    print(
        f"Saved {len(output)} chunks"
    )


if __name__ == "__main__":
    main()