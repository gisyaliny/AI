# Deploy Open-Source LLMs Locally with Ollama & AnythingLLM

Running large language models (LLMs) on your own machine gives you complete privacy, zero API costs, and the freedom to experiment offline. This tutorial walks you through the entire local AI stack — from installing your first model with **Ollama**, to building a private document Q&A system with **AnythingLLM**, and finally publishing your own fine-tuned model to **Hugging Face**.

---

## 1. Why Run LLMs Locally?

| Benefit | Description |
| :--- | :--- |
| **Privacy** | Your data never leaves your machine. Critical for proprietary code, medical records, or sensitive research. |
| **Cost** | No per-token API fees. Run as many queries as your hardware allows. |
| **Offline** | Works on airplanes, in restricted labs, and behind firewalls. |
| **Customization** | Swap models, tweak parameters, and build custom workflows freely. |
| **Latency** | No network round-trip. Responses can be faster for small models on good hardware. |

### System Requirements (Minimum → Recommended)

| Component | Minimum | Recommended |
| :--- | :--- | :--- |
| RAM | 8 GB | 16–32 GB |
| Storage | 10 GB free | 50+ GB (models are large) |
| GPU | Not required (CPU mode) | NVIDIA GPU with 8+ GB VRAM |
| OS | Windows 10+, macOS 12+, Linux | Same |

---

## 2. Ollama: Your Local Model Engine

[Ollama](https://ollama.com/) is a lightweight CLI tool that lets you download and run open-source LLMs with a single command. Think of it as "Docker for LLMs."

### 2.1 Installation

````{tab-set}

```{tab-item} Windows
1. Visit [ollama.com/download](https://ollama.com/download) and download the `.exe` installer.
2. Run the installer and follow the setup wizard.
3. Ollama will appear in your system tray when ready.
```

```{tab-item} macOS
1. Download the `.dmg` from [ollama.com/download](https://ollama.com/download).
2. Drag Ollama to your Applications folder.
3. Open Ollama from Applications — it runs in the menu bar.
```

```{tab-item} Linux
Run the official install script:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
````

Verify your installation:
```bash
ollama --version
```

### 2.2 Downloading Your First Model

Browse the full model library at [ollama.com/library](https://ollama.com/library). Here are popular choices for beginners:

| Model | Size | Best For |
| :--- | :--- | :--- |
| `llama3.2` | ~2 GB | General chat, fast responses |
| `llama3.1:8b` | ~4.7 GB | Balanced quality and speed |
| `qwen2.5:7b` | ~4.4 GB | Multilingual, strong reasoning |
| `codellama:7b` | ~3.8 GB | Code generation and debugging |
| `mistral` | ~4.1 GB | Creative writing, summarization |
| `deepseek-r1:7b` | ~4.7 GB | Deep reasoning and math |
| `llava` | ~4.5 GB | Vision — understands images |
| `nomic-embed-text` | ~274 MB | Text embeddings (for RAG) |

Download a model with `pull`:
```bash
# Download Llama 3.1 (8B parameter version)
ollama pull llama3.1:8b

# Download a lightweight embedding model (needed for RAG later)
ollama pull nomic-embed-text
```

### 2.3 Running a Model (Interactive Chat)

```bash
ollama run llama3.1:8b
```

You'll enter an interactive chat session directly in your terminal:
```
>>> What is the capital of France?
The capital of France is Paris...

>>> /bye
```

**Useful Commands Inside the Chat:**
- Type your question and press Enter to get a response.
- Type `/bye` to exit the session.
- Type `/set parameter num_ctx 4096` to change context window size on the fly.

### 2.4 Essential Ollama CLI Commands

```bash
# List all downloaded models
ollama list

# Show model metadata (parameters, size, quantization)
ollama show llama3.1:8b

# Remove a model to free disk space
ollama rm codellama:7b

# Start the Ollama API server (usually auto-starts)
ollama serve

# Copy/rename a model locally
ollama cp llama3.1:8b my-research-model
```

### 2.5 Using Ollama's REST API (Programmatic Access)

Ollama exposes a local REST API at `http://localhost:11434`. You can call it from any language:

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1:8b",
        "prompt": "Explain quantum computing in 3 sentences.",
        "stream": False
    }
)
print(response.json()["response"])
```

**cURL Example:**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Write a haiku about machine learning.",
  "stream": false
}'
```

### 2.6 Creating Custom Models with Modelfiles

You can create a specialized version of any model by writing a `Modelfile`:

```dockerfile
# Modelfile for a research writing assistant
FROM llama3.1:8b

# Set system personality
SYSTEM """
You are an expert academic research assistant specializing in GIScience
and remote sensing. Always cite methodology precisely and use formal
academic tone. When uncertain, say so rather than hallucinate.
"""

# Increase context window
PARAMETER num_ctx 8192

# Lower temperature for more deterministic outputs
PARAMETER temperature 0.3
```

Build and run your custom model:
```bash
# Create the custom model
ollama create research-assistant -f Modelfile

# Run it
ollama run research-assistant
```

---

## 3. AnythingLLM: A Private Document Q&A System (RAG)

[AnythingLLM](https://anythingllm.com/) is a desktop application that connects to your local Ollama models and lets you chat with your own documents — PDFs, Word files, code repositories, and more. This is called **Retrieval-Augmented Generation (RAG)**.

### 3.1 How RAG Works (For Beginners)

```
Your Documents  →  Split into Chunks  →  Convert to Embeddings  →  Store in Vector DB
                                                                          ↓
    Your Question  →  Find Relevant Chunks  →  Feed to LLM  →  AI Answer (with sources!)
```

Instead of the LLM guessing from its training data, RAG forces it to **look up your actual documents first**, then generate an answer based on what it found. This dramatically reduces hallucination.

### 3.2 Installing AnythingLLM

1. Visit [useanything.com](https://useanything.com/) and download the desktop app for your OS.
2. Install and launch it. You'll see a setup wizard.

**Docker Alternative:**
```bash
docker pull mintplexlabs/anythingllm
docker run -d -p 3001:3001 \
  --name anythingllm \
  -v ${HOME}/anythingllm:/app/server/storage \
  mintplexlabs/anythingllm
```

### 3.3 Connecting AnythingLLM to Ollama

During the setup wizard (or in Settings):

1. **LLM Provider**: Select **Ollama**.
   - Base URL: `http://localhost:11434` (default, auto-detected).
   - Model: Choose from your downloaded Ollama models (e.g., `llama3.1:8b`).
2. **Embedding Provider**: Select **Ollama**.
   - Model: Choose `nomic-embed-text` (the embedding model we downloaded earlier).
3. **Vector Database**: Keep the default **LanceDB** (built-in, zero config).

### 3.4 Creating a Workspace & Uploading Documents

1. Click **"New Workspace"** and name it (e.g., "Research Papers").
2. Click the **Upload** icon in your workspace.
3. Drag and drop your files:
   - Supported formats: `.pdf`, `.txt`, `.docx`, `.md`, `.csv`, `.json`, `.py`, `.js`, and more.
4. Click **"Move to Workspace"** to process and embed your documents.
5. Wait for the status to show **"Embedded"** for each file.

### 3.5 Chatting With Your Documents

Once documents are embedded, simply type questions in the chat box:

```
You:  What methodology did the authors use for building extraction?
AI:   Based on the uploaded papers, the authors employed a two-stage approach:
      first using HSV color thresholding for initial segmentation, followed by
      a Mask R-CNN model for refined building footprint extraction...
      [Source: paper_2024_building_extraction.pdf, page 7]
```

The AI will cite which document and page it found the answer in!

### 3.6 Advanced AnythingLLM Features

| Feature | Description |
| :--- | :--- |
| **Multiple Workspaces** | Separate knowledge bases per project (e.g., "Thesis", "Course Prep", "Code Docs"). |
| **Chat Modes** | Switch between "Chat" (conversational) and "Query" (strict document-only answers). |
| **API Access** | AnythingLLM provides its own API at `http://localhost:3001/api` for integrations. |
| **Agent Mode** | Enable web browsing, code execution, and file management agents within AnythingLLM. |
| **Multi-User** | Share your instance with lab mates, each with their own login and workspaces. |

---

## 4. Publishing Models to Hugging Face

Once you've fine-tuned a model or created a useful custom variant, you can share it with the world via the [Hugging Face Hub](https://huggingface.co/).

### 4.1 Setting Up Your Hugging Face Account

1. Sign up at [huggingface.co/join](https://huggingface.co/join).
2. Go to **Settings → Access Tokens → New Token**.
3. Create a token with **Write** access. Copy it — you'll need it shortly.

### 4.2 Installing the Hugging Face CLI

```bash
pip install huggingface_hub transformers
```

### 4.3 Authenticating

```bash
huggingface-cli login
```

Paste your Write token when prompted. This stores credentials locally so you don't need to re-authenticate.

**Alternatively, in Python:**
```python
from huggingface_hub import login
login(token="hf_YOUR_TOKEN_HERE")
```

### 4.4 Uploading a Model (Python API)

If you have a fine-tuned Transformers model saved locally:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load your locally fine-tuned model
model = AutoModelForCausalLM.from_pretrained("./my-finetuned-model")
tokenizer = AutoTokenizer.from_pretrained("./my-finetuned-model")

# Push to Hugging Face Hub
# This creates the repo "your-username/my-research-llm" automatically
model.push_to_hub("your-username/my-research-llm")
tokenizer.push_to_hub("your-username/my-research-llm")
```

### 4.5 Uploading a Model (CLI)

For uploading arbitrary files (GGUF, safetensors, configs):

```bash
# Create a new repository on Hugging Face
huggingface-cli repo create my-research-llm --type model

# Upload all files from a local directory to the repo
huggingface-cli upload your-username/my-research-llm ./my-model-folder .
```

### 4.6 Uploading GGUF Files (Ollama-Compatible Format)

If you've quantized a model into GGUF format (used by Ollama and llama.cpp):

```python
from huggingface_hub import HfApi

api = HfApi()

# Create a repository
api.create_repo("your-username/my-model-gguf", repo_type="model")

# Upload the GGUF file
api.upload_file(
    path_or_fileobj="./my-model.Q4_K_M.gguf",
    path_in_repo="my-model.Q4_K_M.gguf",
    repo_id="your-username/my-model-gguf",
)
```

### 4.7 Writing a Good Model Card

Every model on Hugging Face should have a `README.md` (Model Card). This is critical for discoverability and reproducibility:

```markdown
---
license: apache-2.0
language:
  - en
tags:
  - llama
  - geospatial
  - research
base_model: meta-llama/Llama-3.1-8B
datasets:
  - your-username/your-dataset
---

# My Research LLM

## Model Description
A fine-tuned Llama 3.1 8B model specialized for geospatial research tasks
including building extraction, land use classification, and map analysis.

## Training Details
- **Base Model**: Llama 3.1 8B
- **Fine-tuning Method**: LoRA (rank=16, alpha=32)
- **Training Data**: 50,000 geospatial Q&A pairs
- **Hardware**: 1x NVIDIA A100 80GB
- **Training Time**: ~8 hours

## Usage
```python
from transformers import pipeline
pipe = pipeline("text-generation", model="your-username/my-research-llm")
result = pipe("Describe the land use pattern in this satellite image analysis...")
```

## Evaluation
| Benchmark | Score |
| :--- | :--- |
| GeoQA Accuracy | 87.3% |
| MapReader F1 | 0.92 |

## Limitations
- Optimized for English-language geospatial tasks only.
- May hallucinate specific coordinate values.

## Citation
If you use this model, please cite:
```bibtex
@misc{yang2025geollm,
  title={GeoLLM: A Specialized Language Model for Geospatial Research},
  author={Yang, Eric},
  year={2025}
}
```

---

## 5. End-to-End Workflow: From Download to Deployment

Here is a complete workflow combining everything we've learned:

```
Step 1: Install Ollama
         ↓
Step 2: Pull a base model (e.g., llama3.1:8b)
         ↓
Step 3: Create a custom Modelfile with your system prompt
         ↓
Step 4: Build your custom model with `ollama create`
         ↓
Step 5: Install AnythingLLM
         ↓
Step 6: Connect AnythingLLM → Ollama (localhost:11434)
         ↓
Step 7: Upload your research papers into a Workspace
         ↓
Step 8: Chat with your documents using your custom model!
         ↓
(Optional) Step 9: Fine-tune the model on your domain data
         ↓
(Optional) Step 10: Publish to Hugging Face for the community
```

---

## 6. Troubleshooting Common Issues

| Problem | Solution |
| :--- | :--- |
| `ollama: command not found` | Restart your terminal. On Linux, ensure `/usr/local/bin` is in your PATH. |
| Model download stuck | Check disk space with `df -h`. Models can be 4–50 GB. |
| Slow responses (no GPU) | Use smaller quantized models like `llama3.2` or `qwen2.5:1.5b`. |
| AnythingLLM can't find Ollama | Ensure `ollama serve` is running. Check the URL is `http://localhost:11434`. |
| Out of memory (OOM) | Close other apps. Use a smaller model. Add `PARAMETER num_ctx 2048` to reduce context. |
| CUDA/GPU not detected | Install the [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) and update GPU drivers. |

---

## 7. Curated Resources & Further Reading

### Official Documentation
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/README.md) — Official README with full command reference and API docs.
- [Ollama Model Library](https://ollama.com/library) — Browse and search all available models.
- [AnythingLLM Docs](https://docs.anythingllm.com/) — Official documentation for setup, configuration, and API usage.
- [Hugging Face Hub Documentation](https://huggingface.co/docs/hub/en/index) — Complete guide to uploading, versioning, and sharing models.

### Tutorials & Guides
- [freeCodeCamp: How to Run LLMs Locally with Ollama](https://www.freecodecamp.org/news/how-to-run-open-source-llms-locally-using-ollama/) — Beginner-friendly written tutorial.
- [SitePoint: Local LLMs in Production (2025)](https://www.sitepoint.com/local-llms-2025-ollama/) — Advanced guide on using Ollama in production environments.
- [Hugging Face Course](https://huggingface.co/learn) — Free course covering Transformers, fine-tuning, and model sharing.
- [GGUF Format Explained](https://huggingface.co/docs/hub/en/gguf) — Understanding the model format used by Ollama and llama.cpp.

### Community & Ecosystem
- [Open WebUI](https://github.com/open-webui/open-webui) — Beautiful, feature-rich web interface for Ollama (ChatGPT-like UI).
- [LM Studio](https://lmstudio.ai/) — GUI alternative to Ollama for running local models with a visual interface.
- [Ollama Discord Community](https://discord.gg/ollama) — Ask questions and share configurations with other local LLM enthusiasts.

---

## Knowledge Quiz

**Q1: What is the single command to download and interactively chat with Meta's Llama 3.1 model using Ollama?**
<details>
<summary>Answer</summary>

First pull: `ollama pull llama3.1:8b`, then run: `ollama run llama3.1:8b`. Or simply `ollama run llama3.1:8b` which will auto-pull if not already downloaded.
</details>

**Q2: In AnythingLLM, what is the fundamental difference between "Chat" mode and "Query" mode?**
<details>
<summary>Answer</summary>

"Chat" mode is conversational — the AI uses both its training knowledge and your documents to answer. "Query" mode is strict — the AI ONLY answers based on your uploaded documents. If the answer isn't in your docs, it will say it doesn't know rather than guessing.
</details>

**Q3: When publishing a model to Hugging Face, why is a Model Card (README.md) important?**
<details>
<summary>Answer</summary>

The Model Card describes the model's training data, methodology, intended use, limitations, and evaluation metrics. It is essential for reproducibility, discoverability (search ranking on HF Hub), and ethical transparency. It helps other researchers decide whether the model is appropriate for their use case.
</details>
