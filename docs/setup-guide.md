# Setup Guide (2026 Edition)

Follow these instructions to set up the Python AI engines, configuration keys, and n8n workflows.

---

## 🔑 1. Environment Keys Configuration

1. Locate the file `python-chatbot/.env.example`.
2. Copy/rename it to `python-chatbot/.env`:
   ```bash
   cp python-chatbot/.env.example python-chatbot/.env
   ```
3. Open `.env` and fill in your API key values:
   ```env
   OPENAI_API_KEY=sk-proj-yourOpenAiKeyHere...
   ANTHROPIC_API_KEY=sk-ant-api03-yourAnthropicKeyHere...
   ```

---

## 🐍 2. Python Environment Setup

We recommend using a Python virtual environment.

```bash
# Navigate to the python directory
cd python-chatbot

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Running the Python CLI Chatbot (Multi-Provider)
Start the interactive session:
```bash
python ai_chatbot.py
```
*Options:* Select your provider (OpenAI / Anthropic), switch models mid-conversation by typing `switch`, or exit by typing `quit`.

### Running the Content Creator Agent CLI
To generate content interactively:
```bash
python content_creator.py
```
To generate content automatically via command line arguments:
```bash
python content_creator.py "Topic Title" "Blog Post" "Developers" "Professional" "openai"
```
Generated content will be saved automatically in `python-chatbot/output/` as markdown files.

---

## ⚙️ 3. n8n Automation Workflows Setup

### Prerequisites
Install Node.js (v18+) and npm on your system.

### Installing and Launching n8n
Install globally:
```bash
npm install -g n8n
```
Start n8n:
* Double-click `start-n8n.bat` in the project root OR
* Run `n8n start` in your terminal.

### Importing Workflow JSON Templates
1. Open n8n in your web browser (typically `http://localhost:5678`).
2. Click **Workflows** on the left menu, then click **Add Workflow** (or **New**).
3. Open the workflow settings and choose **Import from File**.
4. Import the templates:
   - `n8n-workflows/simple-chatbot-workflow.json`
   - `n8n-workflows/content-creator-workflow.json`
5. Configure your Credentials:
   - Double-click the **OpenAI** / **Anthropic** chat nodes and select/create your API credentials.
6. Click **Activate** (top-right toggle switch) to enable webhook triggers.

---

## 🧪 4. Testing Your Setup

Use the built-in test scripts:
```bash
# Run local CLI chatbot verification
python examples/test_chatbot.py

# Run unified API and n8n webhook communication check
python examples/test_ai_services.py
```