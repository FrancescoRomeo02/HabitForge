from pydantic import BaseModel

class HabitText(BaseModel):
    text: str
    