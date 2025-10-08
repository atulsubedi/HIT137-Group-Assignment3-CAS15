# ai_integration.py
from transformers import pipeline
from PIL import Image
import numpy as np


class AIIntegration:
    def __init__(self):
        """Initialise AI models once for reuse (efficient)."""
        self.text_model = pipeline("sentiment-analysis")
        self.image_model = pipeline(
            "image-classification", model="google/vit-base-patch16-224"
        )

    def run_text_model(self, text: str) -> str:
        """Run sentiment analysis on text input."""
        if not text.strip():
            return "No text provided."
        results = self.text_model(text)
        return f"Sentiment: {results[0]['label']} (confidence {results[0]['score']:.2f})"

    def run_image_model(self, file_path: str) -> str:
        """Run image classification on an image file."""
        try:
            img = Image.open(file_path)
            img = img.resize((224, 224)).convert("RGB")
            arr = np.array(img) / 255.0
            results = self.image_model(
                Image.fromarray((arr * 255).astype("uint8")))
            best = results[0]
            return f"Prediction: {best['label']} (confidence {best['score']:.2f})"
        except Exception as e:
            return f"Image processing failed: {e}"
