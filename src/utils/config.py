"""Configuration management for the Campus AI Chat Platform."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Hugging Face Configuration
    hf_token: Optional[str] = None
    hf_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8080
    max_concurrent_users: int = 3
    
    # Model Configuration
    model_path: str = "./models"
    use_gpu: str = "auto"
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/server.log"
    
    class Config:
        env_file = "config.env"  # Using config.env to avoid conflict with .env venv
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
