from pydantic import BaseModel

class HabitText(BaseModel):
    """
    Model for habit text.
    """
    description: str
    action: str
    quantity: str
    target: str
    frequency: int


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "description": "I plan to meditate every morning for 10 minutes.",
                "action": "meditate",
                "quantity": "10 minutes",
                "target": "every morning",
                "frequency": 7
            }
        }
    def __str__(self):
        return self.description

    def __repr__(self):
        return f"HabitText(description={self.description}, action={self.action}, quantity={self.quantity}, target={self.target}, frequency={self.frequency})"
