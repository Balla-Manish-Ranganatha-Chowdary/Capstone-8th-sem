import json
import logging
from typing import Dict, Any, List

from LLM.api_client import CausalityPredictor
from LLM.prompts import CHAT_SYSTEM_PROMPT, META_SUMMARIZATION_PROMPT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RLMContextManager:
    """
    Recursive Language Model context manager.
    Maintains a multi-level memory hierarchy for extended conversations.
    """
    def __init__(
        self, 
        predictor: CausalityPredictor,     
        hot_window_size: int = 10,         
        warm_window_size: int = 20,        
        max_context_tokens: int = 3500     
    ):
        self.predictor = predictor
        self.hot_window_size = hot_window_size
        self.warm_window_size = warm_window_size
        self.max_context_tokens = max_context_tokens
        self.reset()

    def reset(self) -> None:
        """Clear all memory levels, keep predictor."""
        self.anchor_document = ""
        self.session_context = ""
        self.hot_memory: List[Dict[str, str]] = []
        self.warm_summaries: List[str] = []
        self.cold_summary: str = ""

    def _format_risk_as_anchor(self, risk_dict: dict) -> str:
        """Converts full JSON risk dict to readable bulleted text."""
        lines = []
        lines.append(f"State: {risk_dict.get('state', 'Unknown')}")
        lines.append(f"Period: {risk_dict.get('period', 'Unknown')}")
        lines.append(f"Analysis Summary: {risk_dict.get('analysis_summary', 'N/A')}\n")
        
        lines.append("Predicted Risks:")
        for risk in risk_dict.get('predicted_risks', []):
            lines.append(f"- Calamity: {risk.get('calamity')} (Risk Level: {risk.get('risk_level')}, Confidence: {risk.get('confidence_score')})")
            lines.append(f"  Basis: {risk.get('confidence_basis')}")
            lines.append(f"  Affected Classes: {', '.join(risk.get('affected_classes', []))}")
            lines.append(f"  Historical Precedent: {risk.get('historical_precedent', 'None')}")
            lines.append("  Preventive Measures:")
            for k, v in risk.get('preventive_measures', {}).items():
                lines.append(f"    - {k.title()}: {', '.join(v)}")
        
        lines.append(f"\nCross-Risk Interactions: {risk_dict.get('cross_risk_interactions', 'None')}")
        lines.append(f"Monitoring Recommendations: {', '.join(risk_dict.get('monitoring_recommendations', []))}")
        lines.append(f"Data Limitations: {risk_dict.get('data_limitations', 'None')}")
        
        return "\n".join(lines)

    def initialize_session(self, risk_prediction: dict, state: str, period: str) -> None:
        """Initializes conversation anchor and session context."""
        self.reset()
        
        self.anchor_document = self._format_risk_as_anchor(risk_prediction)
        
        risks = risk_prediction.get('predicted_risks', [])
        risk_summary = ", ".join([f"{r['calamity']} ({r['confidence_score']:.2f})" for r in risks])
        
        self.session_context = (
            f"Environmental risk analysis session for {state} ({period}).\n"
            f"Key risks identified: {risk_summary}."
        )

    def _summarize_turns(self, turns_text: str) -> str:
        """Uses meta-prompting to summarize given text."""
        messages = [
            {"role": "system", "content": META_SUMMARIZATION_PROMPT.strip()},
            {"role": "user", "content": turns_text}
        ]
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.predictor.generate(messages, max_new_tokens=400, temperature=0.3)
                return response.strip()
            except Exception as e:
                logging.warning(f"Summarization attempt {attempt+1} failed: {e}")
                
        logging.error("Summarization completely failed, returning raw string stub.")
        return "[Error: Could not generate summary]"

    def compress_hot_to_warm(self) -> None:
        """Compresses oldest turns into a warm summary."""
        oldest_turns = self.hot_memory[:self.hot_window_size]
        turns_text = "\n".join([f"{m['role'].title()}: {m['content']}" for m in oldest_turns])
        
        summary = self._summarize_turns(turns_text)
        self.warm_summaries.append(summary)
        
        self.hot_memory = self.hot_memory[self.hot_window_size:]

    def compress_warm_to_cold(self, threshold: int = 5) -> None:
        """Squashes warm summaries into a single cold summary."""
        if len(self.warm_summaries) >= threshold:
            history_text = "\n---\n".join(self.warm_summaries)
            if self.cold_summary:
                history_text = f"Previous Cold Summary:\n{self.cold_summary}\n\n" + history_text
                
            self.cold_summary = self._summarize_turns(history_text)
            self.warm_summaries.clear()

    def build_context(self) -> str:
        """Compiles the multi-level memory into the system context."""
        context_parts = []
        
        context_parts.append("=== ANALYSIS ANCHOR (Always Reference This) ===")
        context_parts.append(self.anchor_document)
        
        context_parts.append("\n=== SESSION SUMMARY ===")
        context_parts.append(self.cold_summary if self.cold_summary else self.session_context)
        
        if self.warm_summaries:
            context_parts.append("\n=== RECENT CONVERSATION CONTEXT ===")
            context_parts.append("\n---\n".join(self.warm_summaries))
            
        return "\n".join(context_parts)

    def chat(self, user_message: str) -> str:
        """Processes a new user query and manages context flow."""
        
        # 1. Build dynamic context message
        context_string = self.build_context()
        
        # 2. Construct messages structure
        messages = [
            {"role": "system", "content": CHAT_SYSTEM_PROMPT.strip()},
            {"role": "system", "content": context_string}
        ]
        messages.extend(self.hot_memory)
        messages.append({"role": "user", "content": user_message})
        
        # Token Check (naive estimation based on string length // 4 to leave generation headroom)
        total_len = sum(len(m['content']) for m in messages)
        estimated_tokens = total_len // 4
        
        logging.debug(f"Estimated conversation tokens before generation: {estimated_tokens}")
        
        # 3. Predictor call
        try:
            assistant_response = self.predictor.generate(messages, temperature=0.5, max_new_tokens=1024)
        except Exception as e:
            logging.error(f"Chat generation error: {e}")
            return "I encountered an error trying to respond. Can you repeat that?"
            
        # 4. Append to hot memory
        self.hot_memory.append({"role": "user", "content": user_message})
        self.hot_memory.append({"role": "assistant", "content": assistant_response})
        
        # 5. Threshold checks
        if len(self.hot_memory) >= (self.hot_window_size * 2): # allow hot memory buffer
            logging.info("Compressing hot memory to warm memory.")
            self.compress_hot_to_warm()
            
        if len(self.warm_summaries) >= 5:
            logging.info("Compressing warm memories to cold summary.")
            self.compress_warm_to_cold(threshold=5)
            
        return assistant_response

    def get_session_stats(self) -> dict:
        total_content = sum(len(m['content']) for m in self.hot_memory) + len(self.anchor_document) + len(self.cold_summary) + sum(len(w) for w in self.warm_summaries)
        
        return {
            'total_turns': len(self.hot_memory) // 2,
            'hot_turns': len(self.hot_memory),
            'warm_summaries': len(self.warm_summaries),
            'cold_summary_exists': bool(self.cold_summary),
            'estimated_context_tokens': total_content // 4
        }

    def export_session(self, path: str) -> None:
        """Serializes current session state."""
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        data = {
            "anchor": self.anchor_document,
            "session_context": self.session_context,
            "cold_summary": self.cold_summary,
            "warm_summaries": self.warm_summaries,
            "hot_memory": self.hot_memory
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

def get_chat_session(risk_prediction: dict, state: str, period: str, predictor: CausalityPredictor = None) -> RLMContextManager:
    """Helper method required for streamlit integration."""
    
    # Ideally, streamlit provides the predictor or we initialize a mocked/global var.
    # For independent operation context it can be passed via args.
    if not predictor:
        raise ValueError("Predictor is required to initialize RLM session.")
        
    manager = RLMContextManager(predictor)
    manager.initialize_session(risk_prediction, state, period)
    return manager

if __name__ == '__main__':
    # Demo execution
    pass
