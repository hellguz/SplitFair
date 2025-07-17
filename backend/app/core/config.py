# ./backend/app/core/config.py
"""
Configuration module for the application.
Loads settings from the .env file using Pydantic's BaseSettings.
"""
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'))

class Settings(BaseSettings):
    """
    Defines the application's configuration settings.
    """
    # App settings
    APP_SECRET_KEY: str

    # Database settings
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_HOST: str
    
    # Backend settings
    BACKEND_BASE_URL: str

    # Frontend settings
    FRONTEND_ORIGIN: str

    class Config:
        case_sensitive = True

# Create a single instance of the Settings class
settings = Settings()

