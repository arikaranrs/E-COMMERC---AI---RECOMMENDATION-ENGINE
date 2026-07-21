import sys
import os

# Add backend folder to Python module search path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

# Import the FastAPI app instance from backend/app/main.py
from app.main import app
