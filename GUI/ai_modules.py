from transformers import pipeline

def ai_models():
    text_model = pipeline("sentiment-analysis")
    img_model = pipeline("image-classification", model="google/vit-base-patch16-224")
    return text_model, img_model