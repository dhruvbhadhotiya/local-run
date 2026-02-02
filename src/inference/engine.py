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
        Load the language model from local storage or download from Hugging Face.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            logger.info(f"Loading model: {settings.hf_model}")
            
            # Create models directory if it doesn't exist
            model_dir = Path(settings.model_path)
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # For TinyLlama, we need the GGUF format for llama-cpp-python
            model_file = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
            model_path = model_dir / model_file
            
            # Download model if not present
            if not model_path.exists():
                logger.info("Model not found locally. Downloading from Hugging Face...")
                logger.warning("Model download not implemented yet. Please manually download the model.")
                logger.info(f"Expected path: {model_path}")
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
            logger.info("Model loaded successfully!")
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
