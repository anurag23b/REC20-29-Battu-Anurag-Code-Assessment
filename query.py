import os

from dotenv import load_dotenv

import google.generativeai as genai

from retriever import retrieve

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def answer(question):

    chunks = retrieve(question)

    context = "\n\n".join(
        [
            f"[PAGE {c['page']}]\n{c['text']}"
            for c in chunks
        ]
    )

    prompt = f"""
Answer ONLY using the context.

If the answer is not present,
say:

I cannot find sufficient information in the provided corpus.

CONTEXT:

{context}

QUESTION:

{question}

Provide:
1. Answer
2. Sources
"""

    response = model.generate_content(
        prompt
    )

    return response.text


if __name__ == "__main__":

    q = input("Question: ")

    print(answer(q))