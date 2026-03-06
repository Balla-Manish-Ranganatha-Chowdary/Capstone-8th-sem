import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training
)
import warnings
warnings.filterwarnings('ignore')

def get_model_and_tokenizer(model_id: str):
    """
    Loads 4-bit quantized base model and tokenizer for QLoRA fine-tuning.
    Suitable for Qwen2.5-72B or Llama-3.1-70B on appropriate hardware.
    """
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16 # or torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if not tokenizer.pad_token:
        tokenizer.pad_token = tokenizer.eos_token
        
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        use_cache=False # Disabled for gradient checkpointing
    )
    
    model = prepare_model_for_kbit_training(model)
    
    # QLoRA Config
    peft_config = LoraConfig(
        r=64,
        lora_alpha=128,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, peft_config)
    return model, tokenizer

def main():
    """
    Main finetuning execution script utilizing TRL's SFTTrainer.
    Requires `pip install -U trl`.
    """
    print("Initializing QLoRA Fine-Tuning Pipeline...")
    try:
        from datasets import load_dataset
        from trl import SFTTrainer
        from trl import SFTConfig
    except ImportError:
        print("Please install trl: pip install trl datasets")
        return

    model_id = "Qwen/Qwen2.5-72B-Instruct" # Fallback: meta-llama/Llama-3.1-70B-Instruct
    data_path = "data/train.jsonl"
    
    if not os.path.exists(data_path):
        print(f"Training data {data_path} not found. Running generate step...")
        os.makedirs("data", exist_ok=True)
        from LLM.data_prep import build_training_dataset
        build_training_dataset("data/disasters.csv", "data/cnn_output/", data_path)

    # Load Model
    model, tokenizer = get_model_and_tokenizer(model_id)
    model.print_trainable_parameters()
    
    dataset = load_dataset("json", data_files=data_path, split="train")
    # Split for eval
    split_ds = dataset.train_test_split(test_size=0.2, seed=42)
    train_ds = split_ds["train"]
    eval_ds = split_ds["test"]

    # In newer TRL versions, use SFTConfig
    training_args = SFTConfig(
        output_dir="checkpoints/lora_adapter",
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        # max_seq_length=4096,
        fp16=True, # Set bf16=True for Ampere+
        save_steps=100,
        eval_steps=100,
        logging_steps=10,
        packing=False,
        dataset_text_field=None # since we chat template
    )

    def formatting_prompts_func(example):
        output_texts = []
        for i in range(len(example['messages'])):
            messages = example['messages'][i]
            # Assumes conversation format
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
            output_texts.append(text)
        return output_texts

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        args=training_args,
        formatting_func=formatting_prompts_func,
        max_seq_length=4096
    )

    print("Starting training...")
    # trainer.train()  # Commented out for safety as requested
    
    # trainer.model.save_pretrained("checkpoints/lora_adapter")
    # tokenizer.save_pretrained("checkpoints/lora_adapter")
    print("Finished SFT Setup.")

if __name__ == '__main__':
    # Demo execution
    pass
