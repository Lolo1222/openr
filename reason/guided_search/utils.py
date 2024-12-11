from Levenshtein import distance
from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer('/data2/OpenLLMs/sentence-transformers/paraphrase-MiniLM-L6-v2')
model = SentenceTransformer('/data2/OpenLLMs/math-similarity/Bert-MLM_arXiv-MP-class_zbMath')
def compute_similarity(sentences_pair):
    embeddings = model.encode(sentences_pair)
    embedding_1= model.encode(sentences_pair[0], convert_to_tensor=True)
    embedding_2 = model.encode(sentences_pair[1], convert_to_tensor=True)
    return util.pytorch_cos_sim(embedding_1, embedding_2).cpu().numpy()[0][0]

# Lolo1222: for merge similar node
def is_similar_str_pair(str1: str, str2: str, metric="levenshtein_ratio", threshold=0.95) -> bool:
    if metric == "levenshtein_ratio":
        ratio = 1 - distance(str1, str2) / max(len(str1), len(str2))
        return ratio > threshold
    elif metric == "model_cosine":
        return compute_similarity([str1, str2]) > threshold
    return False
