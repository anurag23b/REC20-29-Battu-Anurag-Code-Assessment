import json


def recall_at_k(
    retrieved,
    relevant
):

    retrieved = set(retrieved)

    relevant = set(relevant)

    if len(relevant) == 0:
        return 0

    return (
        len(
            retrieved.intersection(
                relevant
            )
        )
        / len(relevant)
    )


example = {

    "retrieved": [
        "page_10",
        "page_11",
        "page_12"
    ],

    "relevant": [
        "page_10",
        "page_12"
    ]
}

score = recall_at_k(
    example["retrieved"],
    example["relevant"]
)

with open(
    "evaluation/results.json",
    "w"
) as f:

    json.dump(
        {"Recall@K": score},
        f,
        indent=2
    )

print(score)