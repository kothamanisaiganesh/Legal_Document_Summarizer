# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:09:30 2023

@author: CMP
"""

from transformers import pipeline

def summarize_document(document_text, max_length=150):
    summarizer = pipeline("summarization")
    summary = summarizer(document_text, max_length=max_length, min_length=50, length_penalty=2.0)[0]['summary']
    return summary

def main():
    # Read the legal document text from a file or other source
    with open('LegalDocument.txt', 'r') as file:
        document_text = file.read()

    # Generate document summary
    document_summary = summarize_document(document_text)

    # Print or use the document summary
    print("Original Document:")
    print(document_text)
    print("\nDocument Summary:")
    print(document_summary)

if __name__ == "__main__":
    main()
