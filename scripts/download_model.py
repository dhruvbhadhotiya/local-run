#!/usr/bin/env python3
"""
Model Download Script
Downloads GGUF models from HuggingFace Hub automatically
"""

import os
import sys
from pathlib import Path
from huggingface_hub import hf_hub_download
from tqdm import tqdm


# Model configurations
MODELS = {
    "1": {
        "name": "TinyLlama 1.1B (Recommended for testing)",
        "repo_id": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "size": "~668 MB"
    },
    "2": {
        "name": "Phi-2 2.7B (Better quality, more resources)",
        "repo_id": "TheBloke/phi-2-GGUF",
        "filename": "phi-2.Q4_K_M.gguf",
        "size": "~1.6 GB"
    },
    "3": {
        "name": "Mistral 7B (High quality, requires good hardware)",
        "repo_id": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        "filename": "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "size": "~4.1 GB"
    }
}


def get_models_directory():
    """Get the models directory path"""
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "models"
    models_dir.mkdir(exist_ok=True)
    return models_dir


def check_existing_model():
    """Check if a model already exists"""
    models_dir = get_models_directory()
    gguf_files = list(models_dir.glob("*.gguf"))
    
    if gguf_files:
        print("\n✓ Existing model found:")
        for model_file in gguf_files:
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"  • {model_file.name} ({size_mb:.1f} MB)")
        
        response = input("\nDo you want to download a different model? (y/N): ").strip().lower()
        return response == 'y'
    
    return True


def select_model():
    """Interactive model selection"""
    print("\n" + "="*60)
    print("  MODEL SELECTION")
    print("="*60)
    print("\nAvailable models:\n")
    
    for key, model in MODELS.items():
        print(f"[{key}] {model['name']}")
        print(f"    Size: {model['size']}")
        print()
    
    while True:
        choice = input("Select a model (1-3) [1]: ").strip() or "1"
        if choice in MODELS:
            return MODELS[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def download_model(model_config):
    """Download model from HuggingFace"""
    print("\n" + "="*60)
    print("  DOWNLOADING MODEL")
    print("="*60)
    print(f"\nModel: {model_config['name']}")
    print(f"Size: {model_config['size']}")
    print(f"Source: HuggingFace/{model_config['repo_id']}")
    print(f"File: {model_config['filename']}")
    print()
    
    models_dir = get_models_directory()
    
    try:
        # Download with progress bar
        print("Downloading... This may take several minutes.\n")
        
        downloaded_path = hf_hub_download(
            repo_id=model_config['repo_id'],
            filename=model_config['filename'],
            local_dir=models_dir,
            local_dir_use_symlinks=False
        )
        
        # Verify download
        file_path = Path(downloaded_path)
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"\n✓ Download complete!")
            print(f"  Location: {file_path}")
            print(f"  Size: {size_mb:.1f} MB")
            return True
        else:
            print("\n✗ Download failed: File not found after download")
            return False
            
    except Exception as e:
        print(f"\n✗ Download failed: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check your internet connection")
        print("  2. Verify HuggingFace is accessible")
        print("  3. Try again later")
        return False


def update_env_file(model_config):
    """Update config.env file with model information"""
    project_root = Path(__file__).parent.parent
    config_file = project_root / "config.env"  # Using config.env to avoid conflict with .env venv
    env_example = project_root / ".env.example"
    
    if not config_file.exists() and env_example.exists():
        # Copy from example
        import shutil
        shutil.copy(env_example, config_file)
        print(f"\n✓ Created config.env from .env.example")
    
    if config_file.exists():
        # Update MODEL_PATH in config.env
        with open(config_file, 'r') as f:
            lines = f.readlines()
        
        model_path = f"models/{model_config['filename']}"
        updated = False
        
        with open(config_file, 'w') as f:
            for line in lines:
                if line.startswith('MODEL_PATH='):
                    f.write(f'MODEL_PATH={model_path}\n')
                    updated = True
                else:
                    f.write(line)
        
        if updated:
            print(f"✓ Updated config.env with model path: {model_path}")


def main():
    """Main function"""
    print("\n" + "="*60)
    print("  CAMPUS AI CHAT - MODEL DOWNLOADER")
    print("="*60)
    
    # Check for existing models
    if not check_existing_model():
        print("\nKeeping existing model. Setup complete!")
        return 0
    
    # Select model
    model_config = select_model()
    
    # Confirm download
    print(f"\nYou selected: {model_config['name']}")
    print(f"Download size: {model_config['size']}")
    
    confirm = input("\nProceed with download? (Y/n): ").strip().lower()
    if confirm and confirm != 'y':
        print("\nDownload cancelled.")
        return 1
    
    # Download model
    success = download_model(model_config)
    
    if success:
        # Update .env file
        update_env_file(model_config)
        
        print("\n" + "="*60)
        print("  SUCCESS!")
        print("="*60)
        print("\n✓ Model downloaded and configured successfully!")
        print("\nNext steps:")
        print("  1. Review your config.env file")
        print("  2. Start the server: python server.py")
        print("  3. Open browser: http://localhost:8080")
        return 0
    else:
        print("\n" + "="*60)
        print("  DOWNLOAD FAILED")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
