# EndoAgent 🤖

A fully local, autonomous desktop AI assistant powered by Ollama (`qwen2.5:7b`), LangChain tool calling, Playwright browser automation, and Streamlit.

## Features
- **Local LLM Execution**: Uses `qwen2.5:7b` locally via Ollama with zero cloud API dependencies.
- **YouTube Automation**: Controls video playback (search, play, pause, rewind, skip ads) using Playwright.
- **Gmail Automation**: Drafts and sends emails via Gmail SMTP using secure App Passwords.
- **Interactive UI**: Clean chat interface powered by Streamlit.

## Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai) installed with `qwen2.5:7b` pulled:
  ```bash
  ollama run qwen2.5:7b