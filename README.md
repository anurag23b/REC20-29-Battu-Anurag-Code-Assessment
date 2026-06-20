# Defence Procurement RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for answering questions over the Defence Procurement Manual (DPM-2025 Volume II).

The system ingests procurement documents, splits them into searchable chunks, retrieves relevant context for a user query, and uses Gemini 2.5 Flash to generate grounded answers with source citations.

The primary objective is to provide explainable, document-grounded responses while minimizing hallucinations and maintaining transparency through citations.

---

## Features

* PDF document ingestion
* Automatic document chunking
* Context retrieval
* Gemini-powered answer generation
* Source citations
* Unanswerable question handling
* Modular architecture
* Runnable command-line interface

---

## Architecture

```text
DPM-2025-VOLUME-II.pdf
            │
            ▼
     PDF Loader
            │
            ▼
  Recursive Chunking
            │
            ▼
      Chunk Store
(chunks.json)
            │
            ▼
   Context Retrieval
            │
            ▼
    Gemini 2.5 Flash
            │
            ▼
 Answer + Citations
```

---

## System Components

### 1. Document Ingestion

The procurement manual is loaded using PyPDFLoader.

Purpose:

* Extract text from PDF pages
* Preserve page metadata
* Prepare content for chunking

---

### 2. Chunking Strategy

The document is divided into overlapping chunks using RecursiveCharacterTextSplitter.

Configuration:

```python
chunk_size = 1200
chunk_overlap = 150
```

Reasoning:

Procurement and policy documents often contain:

* Definitions
* Conditions
* Exceptions
* Cross references

Larger chunks help preserve context while overlap prevents information loss near chunk boundaries.

---

### 3. Retrieval

The current implementation uses lightweight keyword-based retrieval.

Process:

1. User submits a question.
2. Question terms are extracted.
3. Chunks containing matching terms receive higher scores.
4. Top-ranked chunks are selected.
5. Retrieved chunks are provided to Gemini.

Reasoning:

A lightweight retrieval layer was implemented to ensure a fully runnable end-to-end solution within the interview time constraints.

The architecture is intentionally modular and can be upgraded to:

* FAISS
* Dense Embeddings
* Hybrid Retrieval
* Reranking

without changing the generation layer.

---

### 4. Answer Generation

Gemini 2.5 Flash is used for answer generation.

The model receives:

* User question
* Retrieved document chunks
* Instructions to remain grounded in the provided context

The model is explicitly instructed:

* Not to use external knowledge
* Not to fabricate information
* To provide citations
* To reject unsupported questions

---

### 5. Citation Support

Retrieved chunks contain page metadata.

Responses include references to the originating pages whenever possible.

Example:

```text
Sources:
PAGE 10
PAGE 12
```

This improves explainability and traceability.

---

### 6. Unanswerable Question Handling

The system is designed to avoid hallucinations.

If sufficient evidence is not available in the retrieved context, Gemini is instructed to return:

```text
I cannot find sufficient information in the provided corpus.
```

Example:

Question:

```text
What is the population of Mars?
```

Response:

```text
I cannot find sufficient information in the provided corpus.
```

---

## Project Structure

```text
project/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   └── DPM-2025-VOLUME-II.pdf
│
├── src/
│   ├── ingest.py
│   ├── query.py
│   └── retriever.py
│
├── vectorstore/
│   └── chunks.json
│
└── evaluation/
    ├── metrics.md
    └── results.json
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Build the Corpus

Run:

```bash
python src/ingest.py
```

Expected output:

```text
Saved 570 chunks
```

This creates:

```text
vectorstore/chunks.json
```

which stores the processed document chunks.

---

## Query the System

Run:

```bash
python src/query.py
```

Example:

```text
What are Category-I sensitive sectors?
```

Example output:

```text
Atomic Energy
Broadcasting / Print and Digital Media
Defence
Space
Telecommunications

Sources:
PAGE 10
PAGE 12
```

---

## Example Questions

### Category-I Sensitive Sectors

```text
What are Category-I sensitive sectors?
```

### Category-II Sensitive Sectors

```text
What is Category-II sensitive sector?
```

### Procurement Restrictions

```text
What are the restrictions on procurement?
```

### Manual Applicability

```text
What is the procurement manual applicable to?
```

### Unanswerable Query

```text
What is the population of Mars?
```

---

## Evaluation

Evaluation details are available in:

```text
evaluation/metrics.md
evaluation/results.json
```

The implemented evaluation focuses on:

### Retrieval Evaluation

* Recall@K

Measures whether relevant information is retrieved for a query.

### Manual Answer Validation

Representative questions were evaluated to verify:

* Retrieval quality
* Citation quality
* Grounded responses
* Unanswerable handling

---

## Design Decisions

### Why Chunking?

Entire procurement manuals are too large to pass directly to an LLM.

Chunking:

* Improves retrieval precision
* Reduces prompt size
* Improves answer grounding

---

### Why Gemini 2.5 Flash?

Selected because it provides:

* Strong reasoning
* Fast response times
* Low cost
* Easy API integration

---

### Why Keyword Retrieval?

The goal of the assignment was to deliver a working, explainable, end-to-end RAG system within a limited implementation window.

Keyword retrieval provided:

* Simplicity
* Reliability
* Fast implementation

while preserving a clear upgrade path toward dense retrieval.

---

## Limitations

Current limitations:

1. Retrieval is lexical rather than semantic.
2. No dense embedding retrieval.
3. No FAISS indexing.
4. No reranking stage.
5. Citation granularity is page-level.

---

## Future Improvements

Potential enhancements:

### Retrieval

* FAISS vector search
* Dense embeddings
* Hybrid retrieval
* BM25 + vector search

### Ranking

* Cross-encoder reranking
* Context compression

### Evaluation

* Precision@K
* MRR
* NDCG
* Citation Accuracy
* Grounding Score

### Productionization

* REST API
* Docker deployment
* Automated testing
* Monitoring and observability

---

## Conclusion

This project demonstrates a complete Retrieval-Augmented Generation workflow over the Defence Procurement Manual corpus.

The system successfully:

* Ingests procurement documents
* Retrieves relevant context
* Generates grounded answers
* Provides citations
* Handles unsupported queries

while maintaining a simple, explainable, and extensible architecture suitable for future enhancement.
