# main.py

from fastapi import FastAPI
from .models.HabitText import HabitText

# --- Parte 2: Creare l'Applicazione FastAPI ---
app = FastAPI(
    title="HabitForge API",
    description="API for the HabitForge social habit tracker.",
    version="0.1.0",
)

# Post ENDPOINT
@app.post("/habits/")
async def analyze_habit_text(request: HabitText):
    """
    This endpoint receives the natural language text of a new habit.
    For now, it just prints the text and returns a confirmation message.
    """

    print(f"--> Text received from client: '{request.text}'")

    return {
        "status": "success",
        "message": "Text received and printed to the console.",
        "received_data": request.text
    }