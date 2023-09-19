from transformers import GPTNeoForCausalLM, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")

def process_narrative(narrative_text):
    # Tokenize the input text
    inputs = tokenizer(narrative_text, return_tensors='pt')
    
    # Get the model's predictions
    outputs = model(**inputs)
    
    # Only consider the output embeddings (not the loss)
    embeddings = outputs.last_hidden_state

    # We'll just return the embeddings for now
    return embeddings
