import os
from dotenv import load_dotenv
import openai
import anthropic

# Load environment variables
load_dotenv()

class AIChatbot:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        self.openai_client = None
        self.anthropic_client = None
        
        if self.openai_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_key)
        if self.anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
            
        self.provider = None
        self.model = None
        
        # System Prompt
        self.system_prompt = "You are a helpful and intelligent AI assistant."
        
        # Unified conversation history (excluding separate system instruction for Anthropic API)
        # We store history in a list of {"role": "user"|"assistant", "content": "text"}
        self.conversation_history = []
        
    def select_provider_and_model(self):
        print("--- AI Chatbot Provider Selection ---")
        available_providers = []
        if self.openai_client:
            available_providers.append("openai")
        if self.anthropic_client:
            available_providers.append("anthropic")
            
        if not available_providers:
            print("[WARNING] No API keys found! Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file.")
            return False
            
        print("Available providers:")
        for idx, provider in enumerate(available_providers, 1):
            print(f"{idx}. {provider.upper()}")
            
        # Select provider
        provider_choice = 1
        if len(available_providers) > 1:
            try:
                choice = input(f"Select provider (1-{len(available_providers)}) [Default: 1]: ").strip()
                if choice:
                    provider_choice = int(choice)
            except ValueError:
                pass
        
        selected_provider_idx = min(max(provider_choice - 1, 0), len(available_providers) - 1)
        self.provider = available_providers[selected_provider_idx]
        
        # Select model
        if self.provider == "openai":
            models = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
            print("\nAvailable OpenAI Models:")
            for idx, m in enumerate(models, 1):
                print(f"{idx}. {m}")
            model_choice = 1
            try:
                choice = input(f"Select model (1-{len(models)}) [Default: 1]: ").strip()
                if choice:
                    model_choice = int(choice)
            except ValueError:
                pass
            self.model = models[min(max(model_choice - 1, 0), len(models) - 1)]
            
        elif self.provider == "anthropic":
            models = ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307", "claude-3-opus-20240229"]
            print("\nAvailable Anthropic Models:")
            for idx, m in enumerate(models, 1):
                print(f"{idx}. {m}")
            model_choice = 1
            try:
                choice = input(f"Select model (1-{len(models)}) [Default: 1]: ").strip()
                if choice:
                    model_choice = int(choice)
            except ValueError:
                pass
            self.model = models[min(max(model_choice - 1, 0), len(models) - 1)]
            
        print(f"\n[OK] Active Provider: {self.provider.upper()}")
        print(f"[OK] Active Model: {self.model}\n")
        return True
        
    def get_openai_response(self, user_message):
        # Format history for OpenAI (including system prompt)
        messages = [{"role": "system", "content": self.system_prompt}]
        for turn in self.conversation_history:
            messages.append(turn)
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            ai_response = response.choices[0].message.content
            return ai_response
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
            
    def get_anthropic_response(self, user_message):
        # Format history for Anthropic (system prompt is separate parameter)
        messages = []
        for turn in self.conversation_history:
            messages.append(turn)
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=self.system_prompt,
                messages=messages,
                temperature=0.7
            )
            # Extracted response content
            ai_response = response.content[0].text
            return ai_response
        except Exception as e:
            return f"Anthropic Error: {str(e)}"
            
    def chat(self, user_message):
        if self.provider == "openai":
            response = self.get_openai_response(user_message)
        elif self.provider == "anthropic":
            response = self.get_anthropic_response(user_message)
        else:
            response = "Error: No active AI provider selected."
            
        # Update conversation history on success (only if not an error message)
        if not response.startswith("OpenAI Error:") and not response.startswith("Anthropic Error:") and not response.startswith("Error:"):
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response})
            
        return response
        
    def run(self):
        print("===============================================")
        print("AI Chatbot CLI (OpenAI & Anthropic)")
        print("===============================================")
        
        if not self.select_provider_and_model():
            return
            
        print("Type 'quit' or 'exit' to end the session.")
        print("Type 'switch' to change AI provider/model.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nBot: Goodbye!")
                break
                
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit']:
                print("Bot: Goodbye!")
                break
                
            if user_input.lower() == 'switch':
                print()
                self.select_provider_and_model()
                # Clear conversation history when switching models to prevent context mismatches
                self.conversation_history = []
                print("[SWITCH] Conversation history cleared due to model/provider switch.")
                continue
                
            response = self.chat(user_input)
            print(f"\nBot: {response}\n")

if __name__ == "__main__":
    chatbot = AIChatbot()
    chatbot.run()