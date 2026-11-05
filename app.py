import streamlit as st
from src.assistant import SOURCES, ensure_pdfs, load_chunks, retrieve, answer, PROMPTS

st.set_page_config(page_title="Assistant documentaire PNUD", page_icon="📚")
st.title("Assistant documentaire — PNUD & développement durable")
st.caption("Prototype de recherche dans des publications publiques. Les réponses sont générées par un modèle externe et doivent être vérifiées dans les sources.")
with st.expander("Corpus documentaire"):
    for s in SOURCES: st.markdown(f"- [{s['title']}]({s['page']})")
st.info("Confidentialité : la question et les passages sélectionnés sont envoyés au fournisseur API configuré. N’entrez pas d’informations confidentielles.")
if st.button("Préparer les documents", type="secondary"):
    try:
        with st.spinner("Téléchargement des PDF publics…"): ensure_pdfs()
        st.success("Corpus prêt.")
    except Exception as e: st.error(f"Téléchargement impossible : {e}")
question=st.text_area("Votre question", placeholder="Quels sont les axes prioritaires du programme PNUD en Côte d’Ivoire ?")
mode=st.selectbox("Variante de consigne à expérimenter", list(PROMPTS))
if st.button("Rechercher et répondre", type="primary"):
    if not question.strip(): st.warning("Saisissez une question.")
    else:
        try:
            with st.spinner("Recherche locale dans le corpus…"):
                chunks=load_chunks(); hits=retrieve(question,chunks)
            if not hits: st.warning("Aucun passage pertinent trouvé dans le corpus. Essayez une autre formulation.")
            else:
                st.write("Les extraits ci-dessous seront envoyés au modèle pour rédiger la réponse.")
                with st.spinner("Interrogation du modèle configuré…"): result=answer(question,hits,mode)
                st.subheader("Réponse"); st.write(result)
                st.subheader("Passages retrouvés")
                for i,(c,score) in enumerate(hits,1):
                    with st.expander(f"[S{i}] {c['source']['title']} — page {c['page']} (pertinence {score:.2f})"):
                        st.write(c['text']); st.link_button("Ouvrir le document source",c['source']['page'])
        except Exception as e: st.error(f"La requête n’a pas abouti : {e}")
