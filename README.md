# AI Chatbots and Content Creator Agents | n8n, Python, OpenAI, Anthropic (2026 Edition)

Welcome to your advanced AI development suite! This repository provides multi-provider AI chatbot engines, automated content creator agents, and no-code visual workflows designed to connect Python backend systems directly to n8n automation pipelines.

---

## 🚀 Key Features

*   **Multi-Provider AI Chatbot Engine**: A interactive CLI application supporting both **OpenAI** (GPT-4o, GPT-3.5) and **Anthropic** (Claude 3.5 Sonnet, Claude 3 Haiku) with model switching, conversation memory, and clean exception handling.
*   **AI Content Creator Agent**: A command-line script that generates high-quality marketing copy, blog posts, newsletters, and social media announcements using custom system instructions, automatically saving structured markdown outputs.
*   **No-Code n8n Workflow Automations**: Reusable visual workflow templates for n8n:
    *   **Dynamic Chatbot Webhook Routing**: An n8n flow with conditional logic routing to OpenAI or Anthropic depending on incoming webhook arguments.
    *   **Cooperative Agent Content Pipeline**: A multi-stage pipeline where Anthropic Claude researches and designs the content outline, and OpenAI GPT drafts the final formatted copy.
*   **Robust Diagnostic Framework**: Fully automated local and API integration test suites verifying chatbot instantiation, credentials, and n8n webhook API connectivity.
*   **Structured API Standards**: Formalized API schemas and curl testing payloads for webhook integration.

---

## 📁 Repository Layout

```text
MYFIRSTCHATBOT/
├── python-chatbot/
│   ├── output/                # Directory where generated content is saved
│   ├── .env.example           # Reference environment variables
│   ├── ai_chatbot.py          # Multi-provider interactive chatbot engine
│   ├── chatbot.py             # Simple rule-based chatbot base
│   ├── content_creator.py     # Automated CLI content creator agent
│   └── requirements.txt       # Python dependencies
├── n8n-workflows/
│   ├── simple-chatbot-workflow.json    # Dynamic chatbot webhook flow
│   └── content-creator-workflow.json   # Multi-model content creation pipeline
├── examples/
│   ├── test_chatbot.py        # Validates simple rules & AI chatbot init
│   └── test_ai_services.py    # Validates active LLM keys & n8n webhooks
├── docs/
│   ├── setup-guide.md         # Local setup instructions
│   ├── n8n-guide.md           # Visual node graphs and routing logic
│   └── api-spec.md            # Webhook payload & response structures
└── start-n8n.bat              # Batch script to start n8n on Windows
```

---

## 🛠️ Quick Start

### 1. Setup Python Environment
Create your configuration file and install dependencies:
```bash
# Rename the configuration example file
cp python-chatbot/.env.example python-chatbot/.env

# Open .env and add your OpenAI and Anthropic API keys!

# Install dependencies
pip install -r python-chatbot/requirements.txt
```

### 2. Run Interactive Chatbot
Chat with GPT or Claude:
```bash
python python-chatbot/ai_chatbot.py
```
*Tip: Type `switch` at any prompt to change providers or models, or `quit` to exit.*

### 3. Generate Automated Content
Create articles, newsletters, and scripts:
```bash
# Run interactively:
python python-chatbot/content_creator.py

# Or pass parameters directly:
python python-chatbot/content_creator.py "The Rise of Agentic Workflows" "Blog Post" "Developers" "Professional" "anthropic"
```

### 4. Setup n8n Visual Automation
Start your local n8n server:
```bash
n8n start
```
1. Access the dashboard in your web browser (typically `http://localhost:5678`).
2. Go to **Workflows > Import from File** and select a template from the `n8n-workflows/` folder.
3. Configure your API credentials inside the OpenAI/Anthropic nodes and toggle the workflow to **Active**.

---

## 🧪 Testing and Verification

Verify your configurations and API integrations using the scripts in `examples/`:
```bash
# Test chatbot behaviors locally
python examples/test_chatbot.py

# Verify live API keys and test connections to local n8n webhooks
python examples/test_ai_services.py
```

---

## 📘 Documentation
For in-depth explanations, configuration details, and architecture visual graphs, see:
*   [Setup Guide](file:///C:/Users/RAHUL/.gemini/antigravity/scratch/MYFIRSTCHATBOT/docs/setup-guide.md)
*   [n8n Workflow Guide](file:///C:/Users/RAHUL/.gemini/antigravity/scratch/MYFIRSTCHATBOT/docs/n8n-guide.md)
*   [Webhook API Specification](file:///C:/Users/RAHUL/.gemini/antigravity/scratch/MYFIRSTCHATBOT/docs/api-spec.md)