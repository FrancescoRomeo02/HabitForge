# server.py

from fastapi import FastAPI, HTTPException
from .models.HabitInput import HabitInput, HabitAnalysisResponse
import sys
import os

# Aggiungi il path per importare il modulo NLM
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'NLM'))

try:
    from habit_nalyze import extract_habits_ml
    NLP_AVAILABLE = True
    print("✅ NLP module loaded successfully")
except ImportError as e:
    print(f"⚠️ NLP module not available: {e}")
    NLP_AVAILABLE = False

# --- Parte 2: Creare l'Applicazione FastAPI ---
app = FastAPI(
    title="HabitForge API",
    description="API for the HabitForge social habit tracker.",
    version="0.1.0",
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "nlp_available": NLP_AVAILABLE,
        "version": "0.1.0"
    }

# Post ENDPOINT
@app.post("/habits/analyze", response_model=HabitAnalysisResponse)
async def analyze_habit_text(request: HabitInput):
    """
    This endpoint receives the natural language text of a new habit
    and analyzes it to extract action, quantity, frequency, etc.
    """
    
    print(f"--> Text received from client: '{request.text}'")
    
    try:
        if NLP_AVAILABLE:
            # Usa il modulo NLP per analizzare il testo
            analysis = extract_habits_ml(request.text)
            
            return HabitAnalysisResponse(
                status="success",
                message="Habit analyzed successfully using ML",
                original_text=request.text,
                analysis={
                    "action": analysis.get("action"),
                    "quantity": analysis.get("quantities", [{}])[0] if analysis.get("quantities") else None,
                    "target": analysis.get("target"),
                    "frequency_count": analysis.get("frequency_count"),
                    "frequency_period": analysis.get("frequency_period"),
                    "frequency_text": analysis.get("frequency_text"),
                    "language": analysis.get("language"),
                    "confidence": analysis.get("ml_confidence", 0.0)
                }
            )
        else:
            # Fallback: analisi semplice senza ML
            return HabitAnalysisResponse(
                status="success",
                message="Text received (NLP not available)",
                original_text=request.text,
                analysis=None
            )
            
    except Exception as e:
        print(f"❌ Error analyzing habit: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error analyzing habit: {str(e)}"
        )
