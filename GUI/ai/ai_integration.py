# ai_integration.py, it Uses two Hugging Face pipelines:- (!) Text sentiment (distilbert SST-2), and (2) - Image classification (DeiT Tiny)

from transformers import pipeline
from PIL import Image

_text_model = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
_image_model = pipeline(
    "image-classification",
    model="facebook/deit-tiny-patch16-224"
)
def run_text_model(user_text: str) -> str:
    """
    Take a plain string, return a short human-readable result.
    """
    if not isinstance(user_text, str) or not user_text.strip():
        return "Please enter some text."
    res = _text_model(user_text.strip())[0]
    return f"Sentiment: {res['label']} (confidence: {res['score']:.2f})"

def run_image_model(image_path: str) -> str:
    """
    Take a file path to an image, return a short human-readable result.
    """
    if not isinstance(image_path, str) or not image_path.strip():
        return "Please select an image."
    img = Image.open(image_path.strip())
    res = _image_model(img, top_k=1)[0]
    return f"Prediction: {res['label']} (confidence: {res['score']:.2f})"
