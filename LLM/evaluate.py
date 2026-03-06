import json
from typing import List, Dict

def rank_accuracy(predicted_risks: List[Dict], true_disasters: List[Dict], top_k: int = 3) -> float:
    """
    Computes the fraction of actual disasters that appear in the top-K predicted risks.
    """
    if not true_disasters:
        return 1.0  # Perfect if no disasters were expected and maybe model predicted none (or we ignore)
        
    actual_calamities = {d.get('type') for d in true_disasters}
    predicted_top_k = {r.get('calamity') for r in predicted_risks[:top_k] if r.get('calamity')}
    
    hits = len(actual_calamities.intersection(predicted_top_k))
    return hits / len(actual_calamities)

def evaluate_predictions(predictions_file: str, ground_truth_file: str) -> dict:
    """
    Loads JSON lines files and evaluates rank accuracy.
    """
    # ... mock implementation for framework setup
    pass

if __name__ == '__main__':
    # Demo code block
    pass
