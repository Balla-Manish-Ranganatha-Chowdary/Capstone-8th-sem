import json
import random
from typing import Dict, List, Any

# From the prompt requirements
def _format_change_dict(change_dict: dict) -> str:
    """Formats the CNN output into a human-readable summary for the LLM."""
    lines = []
    
    classes = change_dict.get('class_changes', {})
    for cls_name, data in classes.items():
        if data['area_km2_t1'] > 0 or data['area_km2_t2'] > 0:
            lines.append(
                f"- {cls_name.replace('_', ' ').title()}: "
                f"{data['area_km2_t1']:.1f} km2 -> {data['area_km2_t2']:.1f} km2 "
                f"({data['percentage_change']:+.1f}%)"
            )
            
    return "\n".join(lines)

def _format_transitions(change_dict: dict) -> str:
    lines = []
    transitions = change_dict.get('top_transitions', [])
    for t in transitions:
        lines.append(
            f"- {t['from_class'].replace('_', ' ').title()} -> "
            f"{t['to_class'].replace('_', ' ').title()}: "
            f"{t['area_km2']:.1f} km2 ({t['percentage_of_total']:.1f}% of all changes)"
        )
    return "\n".join(lines)

def generate_training_sample(
    state: str,
    start_year: int,
    end_year: int,
    change_dict: dict,
    known_disasters: list
) -> dict:
    """
    Generates a single training sample in chat template format.
    Mocking the generation of the ground-truth response based on known_disasters.
    """
    from LLM.prompts import RISK_PREDICTION_SYSTEM_PROMPT
    
    formatted_changes = _format_change_dict(change_dict)
    formatted_transitions = _format_transitions(change_dict)
    
    user_content = (
        f"State: {state}\n"
        f"Period: {start_year} to {end_year}\n\n"
        f"Land Cover Changes:\n{formatted_changes}\n\n"
        f"Top Land Transitions:\n{formatted_transitions}\n\n"
        "Please analyze these changes and predict natural calamities with risk rankings."
    )
    
    # In a real workflow, this response is curated by domain experts or generated via a stronger teacher model.
    # Here we build a mock structured response matching the expected schema.
    mock_response = {
        "state": state,
        "period": f"{start_year}-{end_year}",
        "analysis_summary": f"Observed changes in {state} indicate shifts in land cover that map to historical disaster records.",
        "predicted_risks": [
            {
                "calamity": d['type'],
                "risk_level": "High" if d['severity'] > 7 else ("Medium" if d['severity'] > 4 else "Low"),
                "confidence_score": round(random.uniform(0.7, 0.95), 2),
                "confidence_basis": f"Historical data shows {d['type']} events in {state} following similar land cover changes.",
                "affected_classes": ["vegetation", "water_bodies"],
                "historical_precedent": f"Recorded severe events in {start_year}-{end_year}.",
                "preventive_measures": {
                    "immediate": ["Alert local disaster management authorities", "Secure vulnerable infrastructure"],
                    "medium_term": ["Reinforce embankments", "Community awareness programs"],
                    "long_term": ["Restore natural buffers", "Update zoning laws"]
                }
            } for d in known_disasters
        ],
        "cross_risk_interactions": "Compounding effects may occur if extreme weather events coincide.",
        "monitoring_recommendations": ["Monitor SWIR bands for soil moisture", "Track vegetation indices monthly"],
        "data_limitations": "Predictions rely on 30m resolution data; highly localized events may be missed."
    }
    
    return {
        "messages": [
            {"role": "system", "content": RISK_PREDICTION_SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": json.dumps(mock_response, indent=2)}
        ]
    }

def build_training_dataset(
    records_csv: str,
    change_data_dir: str,
    output_path: str
) -> None:
    """
    Matches records from the CSV with JSON change dictionaries in change_data_dir
    and writes out a JSONL file suitable for fine-tuning.
    """
    import pandas as pd
    import os
    import glob
    
    if not os.path.exists(records_csv):
        print(f"Warning: {records_csv} not found. Creating a dummy dataset.")
        # This is just for demonstration purposes if file doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(json.dumps(generate_training_sample(
                "Andhra Pradesh", 2019, 2024, 
                {"class_changes": {"vegetation": {"area_km2_t1": 100, "area_km2_t2": 80, "percentage_change": -20}}}, 
                [{"type": "Flood / Flash Flood", "severity": 8}]
            )) + "\n")
        return

    df = pd.read_csv(records_csv)
    
    json_files = glob.glob(os.path.join(change_data_dir, "*.json"))
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for json_file in json_files:
            with open(json_file, 'r') as f:
                change_dict = json.load(f)
                
            state = change_dict.get('state', 'Unknown')
            sys_start = change_dict.get('start_year', 2000)
            sys_end = change_dict.get('end_year', 2024)
            
            # Filter historical disasters for this state and roughly this period
            mask = (df['state'] == state) & (df['year'] >= sys_start) & (df['year'] <= sys_end)
            relevant_disasters = df[mask].to_dict('records')
            
            # Subsample or aggregate disasters to a manageable list
            # We'll just take top 3 by severity if it exists
            if relevant_disasters:
                relevant_disasters = sorted(relevant_disasters, key=lambda x: x.get('severity', 0), reverse=True)[:3]
            else:
                relevant_disasters = [{"type": "Flood / Flash Flood", "severity": 5}] # default fallback

            sample = generate_training_sample(state, sys_start, sys_end, change_dict, relevant_disasters)
            outfile.write(json.dumps(sample) + "\n")
            
    print(f"Dataset generated at {output_path}")

if __name__ == '__main__':
    # Demo execution block
    pass
