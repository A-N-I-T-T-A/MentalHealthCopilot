# utils/shap_explainer.py

import shap
import torch
from model.emotion_classifier import model_loader
from transformers import AutoTokenizer

# Load model and tokenizer
model = model_loader.model
tokenizer = model_loader.tokenizer
id2label = model_loader.id2label  # <-- Get label mapping from model

# Ensure model is in evaluation mode
model.eval()

# Predict function used by SHAP
def predict_prob(texts):
    texts = [str(t) for t in texts]
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    return probs.numpy()

# Initialize SHAP explainer
explainer = shap.Explainer(predict_prob, tokenizer)

# Function to get SHAP explanation with proper output names
def explain_text(text):
    shap_values = explainer([text])
    
    # Assign correct emotion labels to SHAP outputs
    shap_values.output_names = [id2label[i].lower() for i in range(len(id2label))]
    
    return shap_values
