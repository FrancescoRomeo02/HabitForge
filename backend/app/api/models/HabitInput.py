from pydantic import BaseModel
from typing import Optional

class HabitInput(BaseModel):
    """
    Model for habit text input from user.
    """
    text: str
    user_id: Optional[str] = None
    language: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "text": "Voglio correre 5km tutti i giorni",
                "user_id": "user123",
                "language": "it"
            }
        }

class HabitAnalysisResponse(BaseModel):
    """
    Model for the analyzed habit response.
    """
    status: str
    message: str
    original_text: str
    analysis: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Habit analyzed successfully",
                "original_text": "Voglio correre 5km tutti i giorni",
                "analysis": {
                    "action": "correre",
                    "quantity": "5km",
                    "frequency": 7,
                    "period": 7
                }
            }
        }

class HabitDatabaseModel(BaseModel):
    """
    Model for the habit database.
    """
    user_id: int
    name: str
    description: str
    frequency: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "user_id": "123",
                "name": "Correre",
                "description": "correre 5km ogni giorno",
                "frequency": "daily"
            }
        }
