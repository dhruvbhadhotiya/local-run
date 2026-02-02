# Campus-Local AI Chat Platform

A locally deployed AI-powered web platform that operates entirely within a campus Wi-Fi network, enabling students to interact with a large language model hosted on local infrastructure without requiring cloud services.

## 🎯 Overview

This platform provides:
- **Local AI Access**: Chat with a ~1B parameter language model running on campus infrastructure
- **Data Privacy**: All interactions stay within the campus network
- **Real-time Streaming**: See responses generate token-by-token
- **Educational Value**: Learn about AI deployment and infrastructure
- **Simple Setup**: Automated installation with minimal manual configuration

## ✨ Features

- Real-time AI chat interface accessible via web browser
- Streaming responses for better user experience
- Support for 2-3 concurrent users
- No authentication required (Phase 1 MVP)
- No data persistence (privacy-focused)
- Runs entirely on local infrastructure

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- 8GB RAM minimum (16GB recommended)
- 5GB available disk space
- Campus Wi-Fi connection

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd local_run
   ```

2. **Run the setup script** (Coming in Phase 4)
   ```bash
   python setup.py
   ```

3. **Start the server**
   ```bash
   python server.py
   ```

4. **Access the interface**
   - Open browser and navigate to `http://<server-ip>:8080`

## 📋 Current Status

**Phase 1** (In Progress): Project Setup & Backend Foundation
- ✅ Repository structure
- ✅ Documentation files
- 🔄 Backend implementation
- ⏳ Model loading
- ⏳ API endpoints

## 🛠️ Tech Stack

- **Backend**: Python + FastAPI
- **Inference**: llama-cpp-python / transformers
- **Model**: TinyLlama-1.1B-Chat
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Streaming**: Server-Sent Events (SSE)

## 📖 Documentation

- [Product Requirements Document](PRD.md)
- [Development Roadmap](roadmap.md)
- Setup Guide (Coming soon)
- Troubleshooting (Coming soon)

## 🤝 Contributing

Contributions are welcome! This is an educational project designed to help students learn about AI deployment.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for model hosting and libraries
- TinyLlama team for the excellent small language model
- Open-source AI community

---

**Made with ❤️ for campus learning**
