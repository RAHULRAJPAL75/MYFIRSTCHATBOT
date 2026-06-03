import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python-chatbot'))

from chatbot import SimpleChatbot
from ai_chatbot import AIChatbot

def test_simple_chatbot():
    """Test the simple rule-based chatbot"""
    bot = SimpleChatbot()
    
    test_cases = [
        ("hello", "Hi there! How can I help you today?"),
        ("how are you", "I'm doing great! Thanks for asking."),
        ("help", "Available commands: hello, how are you, what can you do, bye, help"),
        ("random text", "I'm not sure how to respond to that. Type 'help' for available commands.")
    ]
    
    print("[TEST] Testing Simple Chatbot...")
    for user_input, expected in test_cases:
        response = bot.get_response(user_input)
        status = "[PASS]" if response == expected else "[FAIL]"
        print(f"{status} Input: '{user_input}' -> Response: '{response}'")

def test_ai_chatbot_initialization():
    """Test standard initialization of the new AIChatbot class"""
    print("\n[TEST] Testing AI Chatbot Initialization...")
    try:
        bot = AIChatbot()
        print("[PASS] AIChatbot instantiated successfully!")
        print(f"   OpenAI Key loaded: {'Yes' if bot.openai_key else 'No'}")
        print(f"   Anthropic Key loaded: {'Yes' if bot.anthropic_key else 'No'}")
    except Exception as e:
        print(f"[FAIL] Failed to instantiate AIChatbot: {str(e)}")

if __name__ == "__main__":
    test_simple_chatbot()
    test_ai_chatbot_initialization()