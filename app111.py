import streamlit as st
from transformers import pipeline, AutoTokenizer
import PyPDF2
import math

# Initialize the summarization pipeline
@st.cache_resource
def load_summarizer():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    return summarizer, tokenizer

summarizer, tokenizer = load_summarizer()

# Function to extract text from uploaded PDF
import PyPDF2
from PyPDF2.errors import PdfReadError

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        
        # Loop through all the pages and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted_text += page.extract_text()

        return extracted_text
    
    except PdfReadError:
        st.error("The uploaded PDF is corrupted or incomplete (EOF marker not found). Please upload a valid PDF.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None


# Function to split text into chunks based on token limits
def split_text_into_chunks(text, tokenizer, max_tokens=1024, overlap=200):
    tokens = tokenizer.encode(text, return_tensors="pt")[0]
    total_tokens = len(tokens)
    chunks = []
    start = 0

    while start < total_tokens:
        end = min(start + max_tokens, total_tokens)
        chunk = tokenizer.decode(tokens[start:end], skip_special_tokens=True)
        chunks.append(chunk)
        # Move start by (max_tokens - overlap) to allow overlap between chunks
        start += (max_tokens - overlap)

    return chunks

# Function to summarize text
def summarize_text(extracted_text, summarizer, tokenizer, max_input_length=1024, detailed=True):
    # Check if extracted_text is empty or too short
    if not extracted_text or len(extracted_text.strip()) == 0:
        st.error("No text was extracted or provided for summarization.")
        return "No text available for summarization."
    
    # Ensure the extracted_text is within a reasonable size for summarization
    if len(extracted_text) > 2000:  # Limit the length of input text
        #st.warning("Input text is too long. It will be truncated.")
        extracted_text = extracted_text[:2000]  # Truncate input text to 2000 characters

    # Tokenize the text and check for token size
    inputs = tokenizer(extracted_text, return_tensors="pt", truncation=True, max_length=max_input_length)
    
    input_length = len(inputs['input_ids'][0])  # Check the tokenized input length
    
    if input_length == 0:
        st.error("Tokenization failed, resulting in empty input.")
        return "Summarization failed due to tokenization error."
    
    # Call the summarizer model with a try-except block
    try:
        # Generate a longer, more detailed summary
        summary = summarizer(extracted_text, max_length=300 if detailed else 150, min_length=150 if detailed else 40, do_sample=False)
        detailed_summary = post_process_summary(summary[0]['summary_text'], extracted_text)
        return detailed_summary
    except IndexError as e:
        st.error(f"Summarization failed: {str(e)}. Check if the input is correctly formatted and tokenized.")
        return "Summarization failed due to index error."
    except Exception as e:
        st.error(f"Error during summarization: {str(e)}")
        return "Summarization failed due to an unexpected error."

# Post-process summary to elaborate
def post_process_summary(summary, extracted_text):
    """
    Post-process the summary by elaborating with key points identified dynamically.
    
    Args:
        summary (str): The generated summary text.
        extracted_text (str): The original text from which the summary was generated.
        
    Returns:
        str: The elaborated summary with key points.
    """
    # Define a dictionary of keywords and their corresponding messages
    key_points = {
        "lease": "The case involves a dispute over a lease agreement.",
        "appeal": "The case went through an appeal process, with important judgments made.",
        "contract": "The case involves issues related to a contract or agreement.",
        "breach": "The case revolves around a breach of contract or obligation.",
        "damages": "The parties are seeking compensation or damages.",
        "liability": "The case examines liability issues among the parties involved.",
        "jurisdiction": "The case involves questions about the appropriate jurisdiction.",
        "settlement": "The case includes discussions of settlement agreements.",
        "fraud": "Allegations of fraud are central to this case.",
        "trust": "The case deals with issues related to trust and fiduciary duties.",
        "property": "The dispute involves questions of property ownership or rights.",
        "arbitration": "The case includes clauses or processes related to arbitration."
    }

    # Start building the elaborated summary
    elaborated_summary = f"Summary:\n{summary}\n\nKey Points from the Original Text:\n"

    # Dynamically check for the presence of keywords in the text
    for keyword, message in key_points.items():
        if keyword in extracted_text:
            elaborated_summary += f"- {message}\n"

    return elaborated_summary



# Streamlit App Layout
def main():
    st.title("Legal Document Summarizer")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from PDF
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        st.subheader("Extracted Text")
        with st.expander("View Extracted Text"):
            st.write(extracted_text)

        # Summarize button
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = summarize_text(extracted_text, summarizer, tokenizer)
            
            st.subheader("Summary")
            st.write(summary)

            # Option to download the summary
            st.download_button(
                label="Download Summary as Text",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()