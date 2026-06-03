import sys
import os
import requests
from dotenv import load_dotenv

# Ensure the python-chatbot path is accessible
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python-chatbot'))

from ai_chatbot import AIChatbot
from content_creator import ContentCreatorAgent

load_dotenv()

def check_local_engines():
    print("[TEST 1] Testing Local Python AI Engines...")
    
    chatbot = AIChatbot()
    creator = ContentCreatorAgent()
    
    openai_available = bool(chatbot.openai_key)
    anthropic_available = bool(chatbot.anthropic_key)
    
    print(f"Key OpenAI Configured: {'[YES]' if openai_available else '[NO]'}")
    print(f"Key Anthropic Configured: {'[YES]' if anthropic_available else '[NO]'}")
    
    if not (openai_available or anthropic_available):
        print("[WARNING] Skipped real API tests because no API keys are loaded. Fill in python-chatbot/.env to enable.")
        return
        
    if openai_available:
        print("\nTesting OpenAI Chatbot Engine...")
        chatbot.provider = "openai"
        chatbot.model = "gpt-3.5-turbo"
        response = chatbot.chat("Say hello in exactly 5 words.")
        print(f"OpenAI Answer: '{response}'")
        
    if anthropic_available:
        print("\nTesting Anthropic Chatbot Engine...")
        chatbot.provider = "anthropic"
        chatbot.model = "claude-3-haiku-20240307"
        response = chatbot.chat("Say hello in exactly 5 words.")
        print(f"Anthropic Answer: '{response}'")
        
    if openai_available:
        print("\nTesting Content Creator Agent (OpenAI)...")
        content = creator.generate_content("n8n Webhook Integration", "Social Media Post", "Developers", "Casual", "openai")
        print(f"OpenAI Content Preview:\n{content[:200]}...\n")
        
def test_n8n_webhooks():
    print("\n[TEST 2] Testing Webhook Communication with local n8n...")
    
    chatbot_webhook_url = "http://localhost:5678/webhook/chatbot"
    content_webhook_url = "http://localhost:5678/webhook/content-creator"
    
    # Test Chatbot Webhook
    payload = {
        "message": "Hello from python script!",
        "provider": "openai",
        "model": "gpt-3.5-turbo"
    }
    
    print(f"Sending POST request to n8n Chatbot: {chatbot_webhook_url}")
    try:
        response = requests.post(chatbot_webhook_url, json=payload, timeout=3)
        print(f"n8n Response Status: {response.status_code}")
        print(f"n8n JSON Output:\n{response.json()}\n")
    except requests.exceptions.ConnectionError:
        print("[FAIL] Could not connect to local n8n.")
        print("Note: Make sure n8n is running (npm install -g n8n & n8n start) and your webhook triggers are active in the browser (http://localhost:5678).")
    except Exception as e:
        print(f"[FAIL] Error occurred: {str(e)}")
        
    # Test Content Creator Webhook
    content_payload = {
        "topic": "Python Webhooks in 2026",
        "content_type": "Blog Post",
        "audience": "Software Engineers",
        "tone": "Informative"
    }
    
    print(f"\nSending POST request to n8n Content Creator: {content_webhook_url}")
    try:
        response = requests.post(content_webhook_url, json=content_payload, timeout=3)
        print(f"n8n Response Status: {response.status_code}")
        print(f"n8n JSON Output:\n{response.json()}\n")
    except requests.exceptions.ConnectionError:
        print("[FAIL] Could not connect to local n8n.")
    except Exception as e:
        print(f"[FAIL] Error occurred: {str(e)}")

if __name__ == "__main__":
    print("=========================================")
    print("Starting AI Services Integration Tests")
    print("=========================================\n")
    check_local_engines()
    test_n8n_webhooks()
    print("\nTesting Finished!")
