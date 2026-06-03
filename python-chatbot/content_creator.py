import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import openai
import anthropic

# Load environment variables
load_dotenv()

class ContentCreatorAgent:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        self.openai_client = None
        self.anthropic_client = None
        
        if self.openai_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_key)
        if self.anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
            
        # Output directory
        self.output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def check_credentials(self):
        if not self.openai_client and not self.anthropic_client:
            print("[WARNING] Error: Neither OpenAI nor Anthropic API keys were found in the environment variables.")
            print("Please create a .env file with OPENAI_API_KEY or ANTHROPIC_API_KEY.")
            return False
        return True
        
    def generate_content(self, topic, content_type, audience, tone, provider, model=None):
        system_prompts = {
            "blog post": "You are a professional content writer. Write a comprehensive, SEO-optimized blog post with headers, key takeaways, and a engaging conclusion.",
            "social media post": "You are a social media copywriter. Generate 3 distinct versions of a post (for LinkedIn, Twitter, and Facebook) using appropriate hashtags, emojis, and hooks.",
            "newsletter": "You are an email marketer. Write an engaging newsletter with an attention-grabbing subject line, a personalized introduction, body paragraphs, and a clear call to action.",
            "video script": "You are a video producer and writer. Write an outline and screenplay script containing visual directions, hook, intro, main teaching points, outro, and call-to-action.",
            "marketing copy": "You are a conversion copywriter. Write persuasive landing page or product description copy utilizing frameworks like AIDA (Attention, Interest, Desire, Action) or PAS (Problem, Agitate, Solve)."
        }
        
        # Default system prompt if content_type is not matched exactly
        system_prompt = system_prompts.get(
            content_type.lower(), 
            f"You are a skilled content creator. Generate premium content of type: '{content_type}'."
        )
        
        prompt = f"""
        Generate content based on the following specifications:
        - Topic: {topic}
        - Content Type: {content_type}
        - Target Audience: {audience}
        - Desired Tone: {tone}
        
        Ensure the output is high-quality, formatted in Markdown, and ready to publish.
        """
        
        if provider == "openai":
            if not self.openai_client:
                return "Error: OpenAI client not initialized. Check your API key."
            selected_model = model or "gpt-4o"
            print(f"Generating content with OpenAI ({selected_model})...")
            try:
                response = self.openai_client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI Error: {str(e)}"
                
        elif provider == "anthropic":
            if not self.anthropic_client:
                return "Error: Anthropic client not initialized. Check your API key."
            selected_model = model or "claude-3-5-sonnet-20241022"
            print(f"Generating content with Anthropic ({selected_model})...")
            try:
                response = self.anthropic_client.messages.create(
                    model=selected_model,
                    max_tokens=2000,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )
                return response.content[0].text
            except Exception as e:
                return f"Anthropic Error: {str(e)}"
        else:
            return f"Error: Unknown provider '{provider}'"
            
    def save_content(self, topic, content_type, audience, tone, provider, content):
        # Create a filename slug
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic.lower()]).strip("_")[:30]
        safe_type = content_type.lower().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{safe_type}_{safe_topic}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        frontmatter = f"""---
title: Content Generation - {topic}
date: {datetime.now().isoformat()}
content_type: {content_type}
audience: {audience}
tone: {tone}
provider: {provider}
generated_by: MYFIRSTCHATBOT Content Creator Agent (2026)
---

"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(content)
            
        return filepath
        
    def run_interactive(self):
        print("===============================================")
        print("AI Content Creator Agent (OpenAI & Anthropic)")
        print("===============================================")
        
        if not self.check_credentials():
            return
            
        # Get topic
        topic = input("Enter Topic (e.g. Python automation, AI trends): ").strip()
        if not topic:
            print("Error: Topic is required.")
            return
            
        # Content types selection
        content_types = ["Blog Post", "Social Media Post", "Newsletter", "Video Script", "Marketing Copy"]
        print("\nSelect Content Type:")
        for idx, ct in enumerate(content_types, 1):
            print(f"{idx}. {ct}")
        try:
            choice = int(input(f"Choice (1-{len(content_types)}) [Default: 1]: ") or 1)
        except ValueError:
            choice = 1
        content_type = content_types[min(max(choice - 1, 0), len(content_types) - 1)]
        
        # Audience
        audience = input("\nEnter Target Audience [Default: General Public]: ").strip() or "General Public"
        
        # Tone
        tones = ["Professional", "Casual", "Informative", "Creative", "Persuasive"]
        print("\nSelect Tone:")
        for idx, t in enumerate(tones, 1):
            print(f"{idx}. {t}")
        try:
            choice = int(input(f"Choice (1-{len(tones)}) [Default: 1]: ") or 1)
        except ValueError:
            choice = 1
        tone = tones[min(max(choice - 1, 0), len(tones) - 1)]
        
        # Select provider
        providers = []
        if self.openai_client:
            providers.append("openai")
        if self.anthropic_client:
            providers.append("anthropic")
            
        print("\nSelect API Provider:")
        for idx, p in enumerate(providers, 1):
            print(f"{idx}. {p.upper()}")
        try:
            choice = int(input(f"Choice (1-{len(providers)}) [Default: 1]: ") or 1)
        except ValueError:
            choice = 1
        provider = providers[min(max(choice - 1, 0), len(providers) - 1)]
        
        print("\n[WAIT] Generating your content... Please wait...")
        result = self.generate_content(topic, content_type, audience, tone, provider)
        
        if result.startswith("OpenAI Error:") or result.startswith("Anthropic Error:") or result.startswith("Error:"):
            print(f"\n[ERROR] Content generation failed:\n{result}")
        else:
            filepath = self.save_content(topic, content_type, audience, tone, provider, result)
            print("\n" + "="*50)
            print("[SUCCESS] Content Generated Successfully!")
            print(f"[FILE] Saved to: {filepath}")
            print("="*50)
            print(result[:500] + "\n... [Content Truncated, see file for full output] ...")
            print("="*50)

if __name__ == "__main__":
    agent = ContentCreatorAgent()
    
    # Check if arguments are passed via command line for non-interactive triggering
    if len(sys.argv) > 1:
        # Example call: python content_creator.py "AI in 2026" "Blog Post" "Developers" "Professional" "openai"
        try:
            topic = sys.argv[1]
            content_type = sys.argv[2] if len(sys.argv) > 2 else "Blog Post"
            audience = sys.argv[3] if len(sys.argv) > 3 else "General Public"
            tone = sys.argv[4] if len(sys.argv) > 4 else "Professional"
            provider = sys.argv[5] if len(sys.argv) > 5 else "openai"
            
            result = agent.generate_content(topic, content_type, audience, tone, provider)
            if not (result.startswith("OpenAI Error:") or result.startswith("Anthropic Error:") or result.startswith("Error:")):
                filepath = agent.save_content(topic, content_type, audience, tone, provider, result)
                print(f"SUCCESS:{filepath}")
            else:
                print(f"FAILED:{result}")
        except Exception as e:
            print(f"ERROR: {str(e)}")
    else:
        agent.run_interactive()
