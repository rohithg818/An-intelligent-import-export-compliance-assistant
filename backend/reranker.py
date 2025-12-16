# backend/reranker.py

from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def cross_encoder_rerank(query, items, top_k):
    pairs = [[query, item["document"]] for item in items]
    scores = cross_encoder.predict(pairs)

    ranked = sorted(
        zip(scores, items),
        key=lambda x: x[0],
        reverse=True
    )

    return [item for _, item in ranked[:top_k]]
