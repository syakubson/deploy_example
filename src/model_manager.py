"""
Model loading and text generation logic for Qwen3.
"""

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class ModelManager:
    """Manager for Qwen3 model loading and text generation."""
    
    def __init__(self):
        """Initialize ModelManager with empty state."""
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
    
    def load_model(self):
        """Load Qwen3 model and tokenizer from local directory."""
        model_path = os.getenv("MODEL_PATH", "/app/model")
        
        print(f"Loading model from {model_path}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                device_map="auto"
            )
            
            self.model_loaded = True
            print("Model loaded successfully")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def generate_text(self, prompt: str, max_new_tokens: int = 32768) -> tuple[str, str]:
        """
        Generate text using Qwen3 model.
        
        Args:
            prompt: Input text prompt
            max_new_tokens: Maximum number of tokens to generate
            
        Returns:
            Tuple of (thinking_content, final_content)
        """
        if not self.model_loaded or self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded")
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=True
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens
        )
        
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
        
        try:
            # Find </think> token (151668)
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0
        
        thinking_content = self.tokenizer.decode(
            output_ids[:index], 
            skip_special_tokens=True
        ).strip("\n")
        content = self.tokenizer.decode(
            output_ids[index:], 
            skip_special_tokens=True
        ).strip("\n")
        
        return thinking_content, content
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model_loaded

model_manager = ModelManager()
