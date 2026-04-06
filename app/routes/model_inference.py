from fastapi import APIRouter, HTTPException, Request
from app.utils.text_preprocessing import clean_text
from app.schemas import TextInput

router = APIRouter(
    prefix="/model",
    tags=["Model inference"]
)

@router.post("/quora/classify")
async def classify_quora_questions(data: TextInput, request: Request):
    try:
        cleaned_text = clean_text(data.text)
        
        # Access pre-loaded models from app.state
        embedder = request.app.state.embedder
        quora_classifier = request.app.state.quora_classifier

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
async def classify_imbd_reviews(data: TextInput, request: Request):
    try:
        cleaned_text = clean_text(data.text)

        # Access pre-loaded models from app.state
        embedder = request.app.state.embedder
        imdb_classifier = request.app.state.imdb_classifier

        embedding = embedder.encode([cleaned_text], convert_to_numpy=True)
        pred = imdb_classifier.predict(embedding)[0]
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
    