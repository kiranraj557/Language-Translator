from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import MBartTokenizer, pipeline
from pymongo import MongoClient
import subprocess
import sys

# Ensure SentencePiece is installed
try:
    import sentencepiece
except ImportError:
    print("SentencePiece not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sentencepiece"])

# Initialize the tokenizer and model globally
tokenizer = MBartTokenizer.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
translator = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt", tokenizer=tokenizer)

# Connect to MongoDB (default localhost connection)
client = MongoClient("mongodb://localhost:27017/")
db = client.translation_db
translations_collection = db.translations

app = FastAPI()

# Define a mapping for supported languages
LANGUAGE_MAP = {
    "hindi": "hi_IN",
    "Korean": "ko_KR"
}

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en_XX"  # Default source language is English
    target_lang: str

@app.post("/translate/")
async def translate(request: TranslationRequest):
    # Ensure the target language is valid
    if request.target_lang not in LANGUAGE_MAP:
        raise HTTPException(status_code=400, detail="Target language not supported.")
    
    # Check if the translation already exists in the database
    existing_translation = translations_collection.find_one({
        "text": request.text,
        "source_lang": request.source_lang,
        "target_lang": request.target_lang
    })
    
    if existing_translation:
        return {"translated_text": existing_translation['translated_text']}
    
    # Set the target language code based on the selected language
    target_lang_code = LANGUAGE_MAP[request.target_lang]
    
    try:
        # Hugging Face's pipeline automatically handles tokenization, translation, and detokenization
        translated = translator(request.text, src_lang=request.source_lang, tgt_lang=target_lang_code)
        
        # Extract the translated text from the result
        translated_text = translated[0]['translation_text']
        
        # Save the translated text to the database
        translations_collection.insert_one({
            "text": request.text,
            "source_lang": request.source_lang,
            "target_lang": request.target_lang,
            "translated_text": translated_text
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
    
    return {"translated_text": translated_text}



