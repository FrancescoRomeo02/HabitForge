#!/usr/bin/env python3
"""
HabitForge Backend Entry Point
"""

import uvicorn
from app.api.server import app

if __name__ == "__main__":
    uvicorn.run(
        "app.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )