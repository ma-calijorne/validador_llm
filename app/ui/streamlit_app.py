from __future__ import annotations

import json
import streamlit as st

from app.rag.retriever import Retriever
from app.rag.prompt_builder import build_rag_prompt
from app.rag.generator import LocalGenerator
from app.evaluation.repository import EvaluationRepository
from app.evaluation.rubric import compute_average_score, suggest_final_decision
from app.common.models import EvaluationRecord


st.set_page_config(page_title="LLM Validation MVP", layout="wide")

st.title("LLM Validation MVP")
st.caption("Ambiente de apoio à validação humana de respostas sobre Enterprise-Grade Data Intelligence")

retriever = Retriever()
generator = LocalGenerator()
repo = EvaluationRepository()

with st.sidebar:
    evaluator_name = st.text_input("Nome do avaliador")
    top_k = st.slider("Top-K recuperação", min_value=3, max_value=10, value=5)

prompt = st.text_area("Prompt avaliado", height=140)
target_response = st.text_area("Resposta do LLM avaliado", height=240)

if st.button("Consultar base RAG"):
    if not prompt.strip():
        st.warning("Informe o prompt.")
    else:
        retrieved = retriever.search(prompt, top_k=top_k)
        rag_prompt = build_rag_prompt(prompt, retrieved)
        rag_response = generator.generate(rag_prompt)

        st.session_state["retrieved"] = retrieved
        st.session_state["rag_response"] = rag_response

if "rag_response" in st.session_state:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resposta do assistente RAG")
        st.write(st.session_state["rag_response"])

    with col2:
        st.subheader("Chunks recuperados")
        for item in st.session_state["retrieved"]:
            with st.expander(f"{item.title} | {item.chunk_id}"):
                st.write(item.text[:2000])
                st.json(item.metadata)

st.subheader("Rubrica de avaliação")

score_correctness = st.slider("Corretude técnica", 1, 5, 3)
score_coverage = st.slider("Cobertura", 1, 5, 3)
score_enterprise_context = st.slider("Aderência ao contexto enterprise", 1, 5, 3)
score_grounding = st.slider("Grounding documental", 1, 5, 3)
score_clarity = st.slider("Clareza", 1, 5, 3)
score_terminology = st.slider("Precisão terminológica", 1, 5, 3)
score_uncertainty = st.slider("Honestidade epistêmica", 1, 5, 3)
score_hallucination_risk = st.slider("Risco de alucinação", 1, 5, 3)

notes = st.text_area("Observações do avaliador", height=120)

scores = {
    "score_correctness": score_correctness,
    "score_coverage": score_coverage,
    "score_enterprise_context": score_enterprise_context,
    "score_grounding": score_grounding,
    "score_clarity": score_clarity,
    "score_terminology": score_terminology,
    "score_uncertainty": score_uncertainty,
    "score_hallucination_risk": score_hallucination_risk,
}

avg_score = compute_average_score(scores)
suggested_decision = suggest_final_decision(avg_score)

st.info(f"Média sugerida: {avg_score:.2f} | Decisão sugerida: {suggested_decision}")

if st.button("Salvar avaliação"):
    retrieved_sources = []
    if "retrieved" in st.session_state:
        for item in st.session_state["retrieved"]:
            retrieved_sources.append(
                {
                    "chunk_id": item.chunk_id,
                    "title": item.title,
                    "source": item.source,
                    "metadata": item.metadata,
                }
            )

    record = EvaluationRecord(
        evaluator_name=evaluator_name or None,
        prompt=prompt,
        target_model_response=target_response,
        rag_assistant_response=st.session_state.get("rag_response"),
        retrieved_sources=json.dumps(retrieved_sources, ensure_ascii=False),
        score_correctness=score_correctness,
        score_coverage=score_coverage,
        score_enterprise_context=score_enterprise_context,
        score_grounding=score_grounding,
        score_clarity=score_clarity,
        score_terminology=score_terminology,
        score_uncertainty=score_uncertainty,
        score_hallucination_risk=score_hallucination_risk,
        final_decision=suggested_decision,
        evaluator_notes=notes or None,
    )

    repo.save(record)
    st.success("Avaliação salva com sucesso.")