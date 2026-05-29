from transformers import AutoTokenizer, AutoModel

# Download model configuration components straight from Hugging Face
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Save the raw components directly to your machine storage disk path
tokenizer.save_pretrained("./local_miniLM_model")
model.save_pretrained("./local_miniLM_model")

print("✅ True HuggingFace model structure successfully written to './local_miniLM_model'!")