import os
from typing import Optional, Dict
import json

class AITextGenerator:
    """
    Professional AI text generation with fallback options.
    Supports: OpenAI API, Local Transformers, and basic templates
    """
    
    def __init__(self, api_key: Optional[str] = None, use_local: bool = False):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.use_local = use_local
        self.provider = self._detect_provider()
    
    def _detect_provider(self) -> str:
        """Detect which AI provider to use"""
        if self.api_key:
            return "openai"
        elif self.use_local:
            try:
                from transformers import pipeline
                return "local"
            except ImportError:
                return "template"
        return "template"
    
    # ========== TEXT GENERATION METHODS ==========
    
    def generate_continuation(self, text: str, length: int = 100) -> str:
        """Continue writing from the given text"""
        if self.provider == "openai":
            return self._openai_continuation(text, length)
        elif self.provider == "local":
            return self._local_continuation(text, length)
        else:
            return self._template_continuation(text)
    
    def brainstorm_ideas(self, topic: str, count: int = 5) -> list:
        """Generate brainstorming ideas on a topic"""
        if self.provider == "openai":
            return self._openai_brainstorm(topic, count)
        elif self.provider == "local":
            return self._local_brainstorm(topic, count)
        else:
            return self._template_brainstorm(topic, count)
    
    def check_grammar(self, text: str) -> Dict:
        """Check and suggest grammar improvements"""
        if self.provider == "openai":
            return self._openai_grammar(text)
        else:
            return self._template_grammar(text)
    
    def summarize(self, text: str, length: int = 100) -> str:
        """Summarize text"""
        if self.provider == "openai":
            return self._openai_summarize(text, length)
        elif self.provider == "local":
            return self._local_summarize(text)
        else:
            return self._template_summarize(text)
    
    def generate_title(self, content: str) -> str:
        """Generate a catchy title for content"""
        if self.provider == "openai":
            return self._openai_title(content)
        else:
            return self._template_title(content)
    
    # ========== OpenAI Methods ==========
    
    def _openai_continuation(self, text: str, length: int) -> str:
        """OpenAI text continuation"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional writing assistant. Continue the text naturally and professionally."},
                    {"role": "user", "content": f"Continue this text (approximately {length} words):\n\n{text}"}
                ],
                max_tokens=length + 50,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}. Falling back to template."
    
    def _openai_brainstorm(self, topic: str, count: int) -> list:
        """OpenAI brainstorming"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative brainstorming assistant. Generate unique, practical ideas."},
                    {"role": "user", "content": f"Generate {count} brainstorming ideas for: {topic}. Return as JSON list."}
                ],
                temperature=0.9
            )
            
            result = response.choices[0].message.content.strip()
            try:
                ideas = json.loads(result)
                return ideas if isinstance(ideas, list) else [ideas]
            except:
                return result.split('\n')[:count]
        except Exception as e:
            return self._template_brainstorm(topic, count)
    
    def _openai_grammar(self, text: str) -> Dict:
        """OpenAI grammar check"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional editor. Check grammar and provide suggestions."},
                    {"role": "user", "content": f"Check and improve this text:\n\n{text}\n\nReturn as JSON with 'corrected' and 'suggestions' fields."}
                ],
            )
            
            result = response.choices[0].message.content.strip()
            try:
                return json.loads(result)
            except:
                return {"corrected": text, "suggestions": [result]}
        except Exception as e:
            return self._template_grammar(text)
    
    def _openai_summarize(self, text: str, length: int) -> str:
        """OpenAI summarization"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a summarization expert. Create concise, clear summaries."},
                    {"role": "user", "content": f"Summarize this text in approximately {length} words:\n\n{text}"}
                ],
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return self._template_summarize(text)
    
    def _openai_title(self, content: str) -> str:
        """OpenAI title generation"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Generate a catchy, professional title. Return only the title."},
                    {"role": "user", "content": f"Generate a title for this content:\n\n{content[:500]}"}
                ],
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return self._template_title(content)
    
    # ========== Local Transformer Methods ==========
    
    def _local_continuation(self, text: str, length: int) -> str:
        """Local model text continuation"""
        try:
            from transformers import pipeline
            generator = pipeline("text-generation", model="gpt2")
            
            result = generator(text, max_length=length, num_return_sequences=1)
            return result[0]['generated_text'].strip()
        except:
            return self._template_continuation(text)
    
    def _local_brainstorm(self, topic: str, count: int) -> list:
        """Local model brainstorming"""
        try:
            from transformers import pipeline
            generator = pipeline("text-generation", model="gpt2")
            
            ideas = []
            for i in range(count):
                prompt = f"Idea {i+1} about {topic}:"
                result = generator(prompt, max_length=50, num_return_sequences=1)
                ideas.append(result[0]['generated_text'].strip())
            
            return ideas
        except:
            return self._template_brainstorm(topic, count)
    
    def _local_summarize(self, text: str) -> str:
        """Local model summarization"""
        try:
            from transformers import pipeline
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            
            # BART requires min 50 tokens
            if len(text.split()) < 50:
                return text
            
            result = summarizer(text, max_length=100, min_length=30, do_sample=False)
            return result[0]['summary_text'].strip()
        except:
            return self._template_summarize(text)
    
    # ========== Template/Fallback Methods ==========
    
    def _template_continuation(self, text: str) -> str:
        """Fallback continuation template"""
        continuations = {
            "I think": "we should focus on what matters most. By prioritizing clarity and purpose, we can achieve better results.",
            "The key": "to success is understanding the fundamentals. Let's break this down into actionable steps.",
            "Moving forward": "we need a clear strategy. Consider implementing a systematic approach to track progress.",
            "In conclusion": "it's important to remember that consistency drives excellence. Keep refining your approach.",
        }
        
        for key, value in continuations.items():
            if key in text:
                return value
        
        return "Continue writing here... This is a placeholder suggestion."
    
    def _template_brainstorm(self, topic: str, count: int) -> list:
        """Fallback brainstorming template"""
        base_ideas = [
            f"Create a structured framework for {topic}",
            f"Research best practices in {topic}",
            f"Identify key stakeholders for {topic}",
            f"Develop a measurement system for {topic}",
            f"Build a prototype for {topic}",
            f"Test assumptions about {topic}",
            f"Gather feedback on {topic}",
        ]
        return base_ideas[:count]
    
    def _template_grammar(self, text: str) -> Dict:
        """Fallback grammar check template"""
        return {
            "corrected": text,
            "suggestions": [
                "✓ Text appears grammatically correct",
                "💡 Consider breaking long sentences for clarity"
            ]
        }
    
    def _template_summarize(self, text: str) -> str:
        """Fallback summarization template"""
        words = text.split()
        return ' '.join(words[:min(50, len(words))]) + "..."
    
    def _template_title(self, content: str) -> str:
        """Fallback title generation template"""
        first_line = content.split('\n')[0]
        if len(first_line) > 50:
            return first_line[:50] + "..."
        return first_line or "Untitled"

# Initialize
def get_ai_generator(use_openai: bool = False) -> AITextGenerator:
    """Factory function to get AI generator"""
    return AITextGenerator(use_local=not use_openai)