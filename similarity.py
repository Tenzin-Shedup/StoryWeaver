import numpy as np
from sklearn.metrics.pairwise import cosine_similarity




def find_top_matches(query_vec, corpus_vecs, top_k=3):
    sims = cosine_similarity([query_vec], corpus_vecs)[0]
    idx = sims.argsort()[::-1][:top_k]
    return [(int(i), float(sims[i])) for i in idx]
