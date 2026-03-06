import json
import logging
import re
from typing import Dict, Any, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

from LLM.prompts import RISK_PREDICTION_SYSTEM_PROMPT
from LLM.data_prep import _format_change_dict, _format_transitions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CausalityPredictor:
    """
    Inference client that wraps the fine-tuned LLM and produces structured 
    risk predictions from CNN change detection output.
    """
    def __init__(self, model_path: str, base_model_id: str = "Qwen/Qwen2.5-72B-Instruct", device: str = 'auto', quantize: bool = True):
        self.device = device
        self.quantize = quantize
        
        logging.info(f"Loading Base Model: {base_model_id}")
        
        bnb_config = None
        if quantize:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16
            )
            
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
        
        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            quantization_config=bnb_config,
            device_map=device,
            trust_remote_code=True
        )
        
        # Load LoRA adapter if path provided
        if model_path and model_path != base_model_id:
            logging.info(f"Loading LoRA Adapter from: {model_path}")
            self.model = PeftModel.from_pretrained(base_model, model_path)
        else:
            self.model = base_model
            
        self.model.eval()

    def _format_prompt(self, change_dict: dict) -> str:
        """Format the change dict into a human-readable user message."""
        state = change_dict.get('state', 'Unknown')
        start_year = change_dict.get('start_year', 2000)
        end_year = change_dict.get('end_year', 2024)
        
        formatted_changes = _format_change_dict(change_dict)
        formatted_transitions = _format_transitions(change_dict)
        
        conf = change_dict.get('segmentation_confidence', {}).get('mean_confidence', 0.0)
        
        prompt = (
            f"State: {state}\n"
            f"Period: {start_year} to {end_year}\n"
            f"Segmentation Confidence: {conf:.2f}\n\n"
            f"Land Cover Changes:\n{formatted_changes}\n\n"
            f"Top Land Transitions:\n{formatted_transitions}\n\n"
            "Please analyze these changes and predict natural calamities with risk rankings."
        )
        return prompt

    def _extract_json(self, text: str) -> dict:
        """Robust parser to extract JSON from model output."""
        # 1. Direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
            
        # 2. Regex extract block
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
                
        # 3. Extract first { ... } block
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
                
        raise ValueError(f"Failed to parse JSON from model output:\n{text}")

    def _validate_schema(self, output: dict) -> bool:
        """Validates output schema against required keys."""
        required_keys = [
            "state", "period", "analysis_summary", "predicted_risks",
            "cross_risk_interactions", "monitoring_recommendations", "data_limitations"
        ]
        
        for key in required_keys:
            if key not in output:
                logging.warning(f"Missing required key in model output: {key}")
                return False
                
        for risk in output.get('predicted_risks', []):
            risk_keys = ["calamity", "risk_level", "confidence_score", "affected_classes"]
            for rk in risk_keys:
                if rk not in risk:
                    logging.warning(f"Missing risk key {rk} in {risk}")
                    return False
                    
        return True

    def generate(self, messages: list, max_new_tokens: int = 2048, temperature: float = 0.1) -> str:
        """Core text generation execution."""
        prompt = self.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        logging.debug(f"Input tokens: {inputs.input_ids.shape[1]}")
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=False,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.pad_token_id
            )
            
        response = outputs[0][inputs.input_ids.shape[1]:]
        return self.tokenizer.decode(response, skip_special_tokens=True)

    def predict_risks(self, change_dict: dict) -> dict:
        """Main entry point to predict risks from CNN metrics."""
        
        user_prompt = self._format_prompt(change_dict)
        
        messages = [
            {"role": "system", "content": RISK_PREDICTION_SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_prompt}
        ]
        
        max_retries = 3
        last_err = None
        
        for attempt in range(max_retries):
            try:
                logging.info(f"Generating risk prediction... Attempt {attempt+1}/{max_retries}")
                raw_output = self.generate(messages)
                
                parsed_json = self._extract_json(raw_output)
                
                if self._validate_schema(parsed_json):
                    # Attach raw input summary for UI convenience
                    parsed_json['input_summary'] = change_dict
                    return parsed_json
                else:
                    raise ValueError("Output failed schema validation.")
                    
            except Exception as e:
                last_err = e
                logging.warning(f"Attempt {attempt+1} failed: {str(e)}")
                
        logging.error("All generation attempts failed.")
        raise RuntimeError(f"Failed to generate valid prediction after {max_retries} retries: {str(last_err)}")

if __name__ == '__main__':
    # Demo code block
    pass
