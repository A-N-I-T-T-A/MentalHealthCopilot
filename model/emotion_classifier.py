# model/emotion_classifier.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

class EmotionClassifier:
    def __init__(self):
        self.model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()
        self.id2label = self.model.config.id2label
        self.label2id = self.model.config.label2id

    def predict_emotion(self, text):
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            outputs = self.model(**tokens)
        probs = F.softmax(outputs.logits, dim=1).squeeze().tolist()
        labels = list(self.id2label.values())
        return sorted(zip(labels, probs), key=lambda x: x[1], reverse=True), outputs.logits

# Export singleton instance
model_loader = EmotionClassifier()
