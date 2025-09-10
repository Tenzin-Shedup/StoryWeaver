from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import torch


GEN_MODEL = 'distilgpt2' # lightweight local model
EMB_MODEL = 'all-MiniLM-L6-v2'


def load_generation_model():
    tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
    model = AutoModelForCausalLM.from_pretrained(GEN_MODEL)
    return tokenizer, model




def generate_text(prompt, tokenizer, model, max_new_tokens=200, temperature=0.8):
    inputs = tokenizer(prompt, return_tensors='pt') 
    with torch.no_grad():
        out = model.generate(
        **inputs,
        do_sample=True,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=0.9,
        )   
    return tokenizer.decode(out[0], skip_special_tokens=True)




_embed_model = None


def get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMB_MODEL)
    return _embed_model




def embed_text(texts):
    model = get_embed_model()
    return model.encode(texts, convert_to_numpy=True)
