# Campus AI Chat Platform

> 🔒 **100% Private** • ⚡ **Real-time Streaming** • 🎯 **One-Command Setup**

A locally deployed AI chat platform for campus networks. All data stays on campus servers with zero cloud dependencies.

---

## ✨ Features

- **🤖 Local AI Inference** - Run AI models entirely on campus hardware
- **💬 Real-time Streaming** - See responses generate token-by-token
- **👥 Multi-user Support** - Handle concurrent users with request queue
- **🎨 Modern UI** - ChatGPT-style interface with dark mode
- **💻 Code Highlighting** - Syntax highlighting for 190+ languages
- **📝 Markdown Support** - Full markdown rendering in responses
- **⚙️ Admin Panel** - Unified CLI for all platform management
- **⚡ Fast Setup** - One command installs everything

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 4GB+ RAM (8GB+ recommended)
- ~1-5GB disk space (depending on model)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/dhruvbhadhotiya/local-run.git
cd local-run

# 2. Run automated setup
python setup.py

# 3. Start the server
# Windows:
.\start.bat

# Linux/Mac:
./start.sh

# 4. Open browser at http://localhost:8080
```

### Admin Control Panel

```bash
# Full platform management
python admin.py
```

---

## ⚙️ Configuration

Edit `config.env` file to customize:

```bash
# Server Settings
HOST=0.0.0.0
PORT=8080
MAX_CONCURRENT_USERS=3

# Model Settings
MODEL_PATH=models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
USE_GPU=false
MAX_TOKENS=512
TEMPERATURE=0.7
```

---

## 🎯 Available Models

| Model | Size | Quality | Use Case |
|-------|------|---------|----------|
| **TinyLlama 1.1B** | ~668 MB | Good | Testing, limited resources |
| **Phi-2 2.7B** | ~1.6 GB | Better | Balanced quality/performance |
| **Mistral 7B** | ~4.1 GB | Best | Production, high quality |

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **AI Engine**: llama-cpp-python
- **Frontend**: Vanilla JS, HTML5, CSS3
- **Libraries**: marked.js (markdown), highlight.js (code)

---

## 📁 Project Structure

```
local-run/
├── frontend/           # Web interface
├── src/               # Backend source code
├── scripts/           # Setup & utility scripts
├── models/            # AI model files
├── logs/              # Application logs
├── admin.py           # Admin control panel
├── setup.py           # One-command installer
├── server.py          # Main application
└── config.env         # Configuration file
```

---

## 🔧 Utility Scripts

```bash
# Platform management
python admin.py

# Download/switch models
python scripts/download_model.py

# Interactive configuration
python scripts/configure.py

# Health check
python scripts/health_check.py
```

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

Made with ❤️ for campus communities
