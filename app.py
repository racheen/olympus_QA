import streamlit as st
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.schema import Document
import json

# Load Document Store
document_store = InMemoryDocumentStore(use_bm25=True)
with open("./documents1.json", "r") as f:
    docs = [Document.from_dict(doc) for doc in json.load(f)]
document_store.write_documents(docs)

# Initialize Retriever and Readers
retriever = BM25Retriever(document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
fine_tuned_reader = FARMReader(model_name_or_path="./fine_tuned_reader_bert", use_gpu=True)

# Pipelines
base_pipe = ExtractiveQAPipeline(reader, retriever)
fine_tuned_pipe = ExtractiveQAPipeline(fine_tuned_reader, retriever)

# Streamlit UI
st.title("Greek Mythology Q&A")
st.write("Ask any question about Greek mythology and get an answer!")

# User input
user_question = st.text_input("Enter your question:")
if user_question:
    with st.spinner("Searching for an answer..."):
        # Run both readers
        base_result = base_pipe.run(query=user_question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}})
        fine_result = fine_tuned_pipe.run(query=user_question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}})
        
        def format_answer(result, label="Answer"):
            if not result["answers"] or result["answers"][0].score < 0.3 or result["answers"][0].answer.strip() == "":
                return f"❌ **{label}**: Out of scope or no confident answer found."
            answer = result["answers"][0]
            return f"✅ **{label}**: {answer.answer} \n\n> _Context:_ {answer.context.strip()[:300]}..."

        st.markdown("### 🔍 Answers")
        st.markdown(format_answer(base_result, "Base Answer"))
        st.markdown(format_answer(fine_result, "Fine-tuned Answer"))

        # Display context carousel using Streamlit tabs
        st.markdown("### 📚 Retrieved Contexts")
        with st.expander("Click to view top retrieved texts"):
            top_docs = base_result.get("documents", [])
            if top_docs:  # Check if we have documents
                for i, doc in enumerate(top_docs[:5]):
                    with st.container():
                        st.markdown(f"**Document {i+1}:**")
                        st.write(doc.content.strip()[:500]) 
                        st.markdown("---")
            else:
                st.write("No documents found.")



