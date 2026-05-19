
# ⚡ Project Dora — Agentic AI Assistant

> A voice-enabled, multilingual AI assistant powered by LLMs, RAG, and real-time web search.

---

## 📋 Table of Contents

- [Requirements](#-requirements)
- [Quick Start](#-quick-start)
  - [1. Create Virtual Environment](#1-create-a-virtual-environment)
  - [2. Activate Virtual Environment](#2-activate-the-virtual-environment)
  - [3. Install Dependencies](#3-install-project-dependencies)
- [Environment Configuration](#-environment-configuration)
- [Running Dora](#-running-dora)

---

## ✅ Requirements

> ⚠️ **This project strictly requires Python `3.11.0`.** Please verify your version before proceeding.

```bash
python --version
# Expected output: Python 3.11.0
```

---

## 🚀 Quick Start

Follow these steps in order to set up your environment and launch the assistant.

### 1. Create a Virtual Environment

Open your terminal in the project root and run the command for your OS:

**Windows**
```bash
python -m venv .venv
```

**macOS / Linux**
```bash
python3 -m venv .venv
```

---

### 2. Activate the Virtual Environment

> 💡 You must activate the environment **before** running or installing anything.
> When active, you'll see `(.venv)` at the start of your terminal prompt.

**Windows — Command Prompt**
```cmd
.venv\Scripts\activate
```

**Windows — PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

---

### 3. Install Project Dependencies

Upgrade `pip` and install all required libraries from `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a file named **`.env`** in the project root directory and populate it with your API keys using the template below:

```env
# ─── User & Assistant Configuration ──────────────────────────
USERNAME="Dev ustaaad"
ASSISTANT_NAME="Dora"
INPUT_LANGUAGE="hi"
ASSISTANT_VOICE="hi-IN-MadhurNeural"

# ─── Core LLM & Inference Providers ──────────────────────────
GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
COHERE_API_KEY="YOUR_COHERE_API_KEY_HERE"
HUGGINGFACE_API_KEY="YOUR_HUGGINGFACE_API_KEY_HERE"

# ─── Search & RAG Tools (Tavily) ──────────────────────────────
TAVILY_API_KEY_1="YOUR_TAVILY_API_KEY_1_HERE"
TAVILY_API_KEY_2="YOUR_TAVILY_API_KEY_2_HERE"
TAVILY_API_KEY_3="YOUR_TAVILY_API_KEY_3_HERE"
```

> 🔒 **Never commit your `.env` file to version control.** Add it to `.gitignore` to keep your keys secure.

---

## 🎯 Running Dora

Once your virtual environment is active and `.env` is configured, launch the assistant:

```bash
python main.py
```
=======
# Mark-1.0
Dora is a futuristic Agentic AI Assistant built to think, talk, search, and act intelligently in real time 🤖✨ Powered by advanced multi-LLM intelligence, voice interaction 🎙️, automation workflows ⚙️, and smart reasoning 🧠, Dora is designed to feel like a real digital companion. From intelligent conversations 💬 and AI-powered search 🌐 

