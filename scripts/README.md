# Campus AI Chat Platform - Scripts

This directory contains utility scripts for setup, configuration, and maintenance.

## Scripts

### `download_model.py`
Automated model downloader from HuggingFace Hub.

**Features:**
- Interactive model selection (3 options)
- Progress tracking
- Automatic .env configuration
- Existing model detection

**Usage:**
```bash
python scripts/download_model.py
```

**Models Available:**
1. TinyLlama 1.1B (~668 MB) - Testing, low resources
2. Phi-2 2.7B (~1.6 GB) - Balanced quality/performance
3. Mistral 7B (~4.1 GB) - Production, high quality

---

### `configure.py`
Interactive configuration wizard with auto-detection.

**Features:**
- GPU auto-detection (CUDA/nvidia-smi)
- RAM-based recommendations
- System capability analysis
- Optimal configuration generation

**Usage:**
```bash
python scripts/configure.py
```

**Auto-detects:**
- GPU availability and model
- RAM capacity
- CPU count
- Performance tier

---

### `health_check.py`
Health monitoring and diagnostics utility.

**Features:**
- Server health check
- Model file verification
- Configuration validation
- Continuous monitoring mode

**Usage:**
```bash
# Single check
python scripts/health_check.py

# Continuous monitoring (every 10 seconds)
python scripts/health_check.py --monitor

# Custom interval (every 30 seconds)
python scripts/health_check.py --monitor 30
```

**Checks:**
- Configuration (.env)
- Model files
- Server health endpoint
- Server status and load

---

## Quick Reference

```bash
# Setup new installation
python setup.py

# Download different model
python scripts/download_model.py

# Reconfigure settings
python scripts/configure.py

# Check system health
python scripts/health_check.py

# Monitor server (Ctrl+C to stop)
python scripts/health_check.py --monitor
```

---

## Requirements

All scripts require the virtual environment to be activated:

```bash
# Windows
.env\Scripts\activate

# Linux/Mac
source .env/bin/activate
```

Some scripts have additional dependencies:
- `configure.py`: psutil, torch (optional for GPU detection)
- `health_check.py`: requests
