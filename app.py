import streamlit as st
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.schema import Document
import json

# Load Document Store
document_store = InMemoryDocumentStore(use_bm25=True)
with open("documents1.json", "r") as f:
    docs = [Document.from_dict(doc) for doc in json.load(f)]
document_store.write_documents(docs)

# Initialize Retriever and Reader
retriever = BM25Retriever(document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
pipe = ExtractiveQAPipeline(reader, retriever)

# Streamlit UI
st.title("Greek Mythology Q&A")
st.write("Ask any question about Greek mythology and get an answer!")

# User input question
user_question = st.text_input("Enter your question:")
if user_question:
    with st.spinner("Searching for an answer..."):
        result = pipe.run(query=user_question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}})
        if result["answers"]:
            st.write(f"**Answer:** {result['answers'][0].answer}")
        else:
            st.write("Sorry, I couldn't find an answer.")
