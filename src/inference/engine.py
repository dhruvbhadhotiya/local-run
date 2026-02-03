"""Model inference engine for the Campus AI Chat Platform."""

import os
from pathlib import Path
from typing import Optional
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from src.utils.config import settings
from src.utils.logger import logger


class ModelEngine:
    """Handles model loading and inference."""
    
    def __init__(self):
        """Initialize the model engine."""
        self.model: Optional[Llama] = None
        self.model_loaded = False
        
    def load_model(self) -> bool:
        """
        Load the language model from local storage.
        Uses MODEL_PATH from config.env for the model file.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            # Get model path from settings (MODEL_PATH in config.env)
            model_path = Path(settings.model_path)
            
            logger.info(f"Loading model from: {model_path}")
            
            # Check if model file exists
            if not model_path.exists():
                # If it's a directory, look for .gguf files
                if model_path.is_dir():
                    gguf_files = list(model_path.glob("*.gguf"))
                    if gguf_files:
                        model_path = gguf_files[0]
                        logger.info(f"Found model: {model_path.name}")
                    else:
                        logger.error(f"No .gguf files found in {model_path}")
                        logger.info("Run: python scripts/download_model.py")
                        return False
                else:
                    logger.error(f"Model not found: {model_path}")
                    logger.info("Run: python scripts/download_model.py")
                    return False
            
            # Load model with llama-cpp-python
            logger.info("Loading model into memory...")
            
            # Determine if we should use GPU
            use_gpu = settings.use_gpu.lower() in ['true', 'auto', 'yes']
            n_gpu_layers = -1 if use_gpu else 0  # -1 means use all layers on GPU
            
            self.model = Llama(
                model_path=str(model_path),
                n_ctx=2048,  # Context window
                n_gpu_layers=n_gpu_layers,
                verbose=False
            )
            
            self.model_loaded = True
            logger.info(f"Model loaded successfully: {model_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model_loaded = False
            return False
    
    def generate(self, prompt: str, max_tokens: Optional[int] = None, 
                 temperature: Optional[float] = None, 
                 top_p: Optional[float] = None) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated text string
        """
        if not self.model_loaded or self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Use defaults from settings if not provided
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        top_p = top_p or settings.top_p
        
        try:
            logger.info(f"Generating response (max_tokens={max_tokens}, temp={temperature})")
            
            # Generate response
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                echo=False,  # Don't echo the prompt
                stop=["</s>", "User:", "\n\n\n"]  # Stop sequences
            )
            
            # Extract generated text
            generated_text = response['choices'][0]['text'].strip()
            
            logger.info(f"Generated {len(generated_text)} characters")
            return generated_text
            
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            raise
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": settings.hf_model,
            "loaded": self.model_loaded,
            "model_path": settings.model_path,
            "max_tokens": settings.max_tokens,
            "temperature": settings.temperature,
            "top_p": settings.top_p
        }


# Global model engine instance
model_engine = ModelEngine()
