import streamlit as st
from models import load_generation_model, generate_text, embed_text
from similarity import find_top_matches
from db_utils import init_db, save_draft
import numpy as np


st.set_page_config(page_title='StoryWeaver')


init_db()


if 'tokenizer' not in st.session_state:
    st.session_state['tokenizer'], st.session_state['model'] = load_generation_model()


st.title('✍️ StoryWeaver — Controlled Creative Writing Coach')


with st.sidebar:
    title = st.text_input('Story title', 'A Quiet Harbor')
    style = st.selectbox('Style', ['literary', 'noir', 'fantasy', 'sci-fi', 'humorous'])
    tone = st.selectbox('Tone', ['wry','wistful','urgent','calm'])
    pacing = st.selectbox('Pacing', ['slow','medium','fast'])
    temp = st.slider('Creativity (temperature)', 0.1, 1.2, 0.8)


seed = st.text_area('✏️ Seed / Current Draft', height=200)


# Outline generation
if st.button('Generate Outline'):
    prompt = f"Create a 5-point outline for a {style} short story titled '{title}'. Tone: {tone}."
    outline = generate_text(prompt, st.session_state['tokenizer'], st.session_state['model'], max_new_tokens=150, temperature=temp)
    st.session_state['outline'] = outline
    st.success('Outline generated!')


outline = st.session_state.get('outline','')
st.subheader('Outline')
st.text_area('Story Outline', outline, height=150)


# Draft expansion
if st.button('Expand Draft'):
    prompt = f"Style: {style}\nTone: {tone}\nPacing: {pacing}\nSeed:\n{seed}\n\nWrite the next scene."
    draft = generate_text(prompt, st.session_state['tokenizer'], st.session_state['model'], max_new_tokens=250, temperature=temp)
    st.session_state['draft'] = draft
    st.text_area('Expanded Draft', draft, height=250)
    save_draft(title, outline, draft, style, tone, pacing)


# Similarity check
if st.button('Check Originality'):
    if seed.strip():
        qvec = embed_text([seed])[0]
        # Dummy reference corpus (2 public-domain samples)
        ref_texts = [
        "It was the best of times, it was the worst of times...",
        "Call me Ishmael. Some years ago..."
        ]
        ref_vecs = embed_text(ref_texts)
        matches = find_top_matches(qvec, ref_vecs, top_k=2)
        st.subheader('Similarity Check')
        for i, score in matches:
            st.write(f"Similarity {score:.2f} → '{ref_texts[i][:50]}...'")
    else:
        st.warning('Please enter some text first.')
