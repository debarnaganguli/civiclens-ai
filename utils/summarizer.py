from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_summarizer():
    # Load the summarization pipeline
    model_name = "Falconsai/text_summarization"
    try:
        summarizer = pipeline("summarization", model=model_name)
        return summarizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def generate_summary(summarizer, text):
    try:
        # Generate summary. Falconsai/text_summarization is based on T5.
        # We ensure it handles appropriate length.
        # If the text is very short, we adjust max_length to avoid errors.
        input_length = len(text.split())
        max_length = min(230, max(30, int(input_length * 0.5)))
        min_length = min(30, max(5, int(input_length * 0.1)))
        
        # Ensure max_length is always strictly greater than min_length
        if max_length <= min_length:
            max_length = min_length + 1
        
        # Max input length for Falconsai is usually 512 tokens.
        # It handles truncation natively if truncation=True is provided.
        result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False, truncation=True)
        return result[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {str(e)}"
