import os
from sklearn.model_selection import train_test_split

# Define the path to your folders
docs_folder = '/Users/kothamanisaiganesh/Desktop/dataset/IN-Abs/train-data/judgement'
summaries_folder = '/Users/kothamanisaiganesh/Desktop/dataset/IN-Abs/train-data/summary'

# Get the list of document filenames
document_files = [f for f in os.listdir(docs_folder) if f.endswith('.txt')]
document_files.sort()

# Create pairs of documents and summaries
documents = []
summaries = []
for doc_file in document_files:
    with open(os.path.join(docs_folder, doc_file), 'r') as doc_f:
        documents.append(doc_f.read())
    
    with open(os.path.join(summaries_folder, doc_file), 'r') as sum_f:
        summaries.append(sum_f.read())

# Split the dataset into training and validation sets (80% train, 20% validation)
train_docs, val_docs, train_summaries, val_summaries = train_test_split(documents, summaries, test_size=0.2, random_state=42)

# Now you have training and validation sets: `train_docs`, `val_docs`, `train_summaries`, `val_summaries`
from transformers import BartTokenizer, BartForConditionalGeneration
from datasets import Dataset
from transformers import Trainer, TrainingArguments

# Load pre-trained BART tokenizer and model
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

# Prepare your dataset in a Hugging Face dataset format
dataset = Dataset.from_dict({
    'document': train_docs,
    'summary': train_summaries
})

# Tokenize the inputs and labels
def tokenize_function(examples):
    inputs = tokenizer(examples['document'], max_length=1024, truncation=True, padding="max_length")
    outputs = tokenizer(examples['summary'], max_length=150, truncation=True, padding="max_length")
    inputs["labels"] = outputs["input_ids"]
    return inputs

# Tokenize the dataset
tokenized_train_dataset = dataset.map(tokenize_function, batched=True)

# Do the same for the validation dataset
val_dataset = Dataset.from_dict({
    'document': val_docs,
    'summary': val_summaries
})

tokenized_val_dataset = val_dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=2,  # Reduced batch size
    per_device_eval_batch_size=2,   # Reduced batch size
    num_train_epochs=3,
    weight_decay=0.01,
)


# Set up the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_val_dataset,
)

# Train the model
trainer.train()
