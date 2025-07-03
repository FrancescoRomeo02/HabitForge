# server.py

from random import randint
from fastapi import FastAPI, HTTPException
from .models.HabitInput import HabitInput, HabitAnalysisResponse,
from app.db.database import HabitRepository
import sys
import os

# Aggiungi il path per importare il modulo NLM
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'NLM'))

extract_habits_ml = None
create_habit_object = None

try:
    from NLM.habit_nalyze import extract_habits_ml, create_habit_object
    NLP_AVAILABLE = True
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
        if NLP_AVAILABLE and extract_habits_ml and create_habit_object:
            # Usa il modulo NLP per analizzare il testo
            analysis = extract_habits_ml(request.text)
            habitObj = create_habit_object(analysis)


            # Save to database
            habit_repo = HabitRepository()
            habit_id = habit_repo.create_habit(
                name=habitObj.name,
                description=habitObj.description,
                frequency=habitObj.frequency,
                user_id=habitObj.user_id
            )
            print(f"✅ Habit saved to database with ID: {habit_id}")   

            return HabitAnalysisResponse(
                status="success",
                message="Habit analyzed successfully",
                original_text=request.text,
                analysis=analysis
            )
        else:
            print("⚠️ NLP module not available, returning default response")
            return HabitAnalysisResponse(
                status="error",
                message="NLP module not available",
                original_text=request.text,
                analysis=None
            )
        

        

            
    except Exception as e:
        print(f"❌ Error analyzing habit: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error analyzing habit: {str(e)}"
        )