import json


def retrieve(question, k=5):

    with open(
        "vectorstore/chunks.json",
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    q_words = set(
        question.lower().split()
    )

    scored = []

    for chunk in chunks:

        score = 0

        text = chunk["text"].lower()

        for word in q_words:

            if word in text:
                score += 1

        scored.append(
            (score, chunk)
        )

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        item[1]
        for item in scored[:k]
    ]