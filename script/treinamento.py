import os
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset

# Nome do modelo base
model_name = "meta-llama/Llama-2-7b-hf"
local_model_path = "../modelo-treinado/llama-2-7b-hf"

# Verifica se o modelo já foi baixado ou treinado
if os.path.exists(local_model_path):
    print(f"Carregando modelo existente de {local_model_path}")
    model = AutoModelForCausalLM.from_pretrained(local_model_path)
    tokenizer = AutoTokenizer.from_pretrained(local_model_path)
else:
    print(f"Baixando o modelo base {model_name}")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    os.makedirs(local_model_path, exist_ok=True)
    model.save_pretrained(local_model_path)
    tokenizer.save_pretrained(local_model_path)

# Configurações de treinamento
training_args = TrainingArguments(
    output_dir="../modelo-treinado",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10,
    save_total_limit=2,
    logging_dir="../logs",
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    save_steps=50,
)

# Carregue os dados de treinamento (certifique-se de ter os arquivos JSONL ou outros suportados)
dataset = load_dataset("json", data_files={"train": "../dataset/train.jsonl", "validation": "../dataset/valid.jsonl"})

# Treinador
trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
)

# Inicia o treinamento
trainer.train()
