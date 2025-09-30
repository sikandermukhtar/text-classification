from fastapi import APIRouter, HTTPException
from app.utils.text_preprocessing import clean_text
from app.schemas import TextInput
import joblib
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent.parent 

quora_classifier_path = BASE_DIR / "model" / "trained_models" / "quora_classifier.pkl"
imdb_classifier_path = BASE_DIR / "model" / "trained_models" / "imdb_classifier.pkl"

router = APIRouter(
    prefix="/model",
    tags=["Model inference"]
)

embedder = SentenceTransformer("all-MiniLM-L6-v2")
quora_classifier = joblib.load(quora_classifier_path)
imdb_classifier = joblib.load(imdb_classifier_path)

@router.post("/quora/classify")
def classify_quora_questions(data: TextInput):
    try:

        cleaned_text = clean_text(data.text)

        embedding = embedder.encode([cleaned_text], convert_to_numpy=True)

        pred = quora_classifier.predict(embedding)[0]
        label = "Insincere" if pred > 0.5 else "Sincere"
        probability = float(pred)

        return {
            "text": data.text,
            "cleaned_text": cleaned_text,
            "label": label,
            "probability": float(probability)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/imbd/classify")
def classify_imbd_reviews(data: TextInput):
    try:

        cleaned_text = clean_text(data.text)

        embedding = embedder.encode([cleaned_text], convert_to_numpy=True)
        print(embedding)
        pred = imdb_classifier.predict(embedding)[0]
        print(pred)
        label = "Positive" if pred > 0.5 else "Negative"
        probability = float(pred) 

        return {
            "text": data.text,
            "cleaned_text": cleaned_text,
            "label": label,
            "probability": float(probability)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    