from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get SECRET_KEY from environment variables
SECRET_KEY = os.getenv('SECRET_KEY')

# Fallback for development (not recommended for production)
if not SECRET_KEY:
    SECRET_KEY = 'django-insecure-your-development-key-here' 