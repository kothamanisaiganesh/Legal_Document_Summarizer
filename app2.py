import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load pre-trained T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Streamlit app layout
st.title('Doubt Clarification ')

# Input for user to enter the content
input_text = st.text_area('Enter the content for Summary ', height=400)

# Button to trigger question generation
if st.button('Generate Questions'):
    if input_text:
        # Tokenize the input text
        inputs = tokenizer.encode("generate questions: " + input_text, return_tensors="pt", max_length=512, truncation=True)

        # Generate questions based on the input content
        outputs = model.generate(inputs, max_length=100, num_return_sequences=3, num_beams=4, no_repeat_ngram_size=2)

        # Decode the generated questions
        generated_questions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

        # Display the generated questions
        st.subheader('Generated Questions')
        for q in generated_questions:
            st.write(f"Q: {q}")

    else:
        st.warning('Please enter the content for question generation')