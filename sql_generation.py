import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

from mysql_operations import get_schema

# Initialize the tokenizer from Hugging Face Transformers library
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql')
model = model.to(device)
model.eval()

# Define the custom database schema
schema = get_schema()
print(schema)


def generate_sql(natural_language_query):
    input_prompt = f"""tables
    {schema}
    query for:{natural_language_query}
    """

    # Combine the schema and query
    input_text = f"{natural_language_query} {input_prompt}"

    # Tokenize the input
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate the SQL query
    output_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)

    # Decode the generated SQL query
    generated_sql = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_sql
