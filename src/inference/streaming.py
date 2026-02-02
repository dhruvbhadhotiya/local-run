"""Streaming inference support for the model engine."""

from typing import AsyncGenerator, Optional
from llama_cpp import Llama
from src.utils.logger import logger


async def stream_generate(
    model: Llama,
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> AsyncGenerator[str, None]:
    """
    Stream generated tokens from the model.
    
    Args:
        model: Loaded Llama model instance
        prompt: Input text prompt
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        
    Yields:
        Generated text tokens one at a time
    """
    try:
        logger.info(f"Starting streaming generation (max_tokens={max_tokens}, temp={temperature})")
        
        # Generate response with streaming
        stream = model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=False,
            stream=True,  # Enable streaming
            stop=["</s>", "User:", "\n\n\n"]
        )
        
        token_count = 0
        
        # Yield tokens as they're generated
        for output in stream:
            if 'choices' in output and len(output['choices']) > 0:
                choice = output['choices'][0]
                
                # Check if generation is complete
                if choice.get('finish_reason') is not None:
                    logger.info(f"Generation complete. Total tokens: {token_count}")
                    break
                
                # Extract and yield the token
                if 'text' in choice:
                    token = choice['text']
                    if token:
                        token_count += 1
                        yield token
        
        if token_count == 0:
            logger.warning("No tokens generated during streaming")
            
    except Exception as e:
        logger.error(f"Error during streaming generation: {str(e)}")
        yield f"[Error: {str(e)}]"
