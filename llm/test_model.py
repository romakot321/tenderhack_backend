import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "IlyaGusev/saiga2_7b_lora"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>\n"
DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."

# Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Тестовый ввод
input_text = "Your input text here."
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

# Приведение модели и данных к одному устройству
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
input_ids = input_ids.to(device)

# Параметры генерации
generation_config = model.generation_config
generation_config.max_new_tokens = 50  # задаем максимальное число токенов

# Генерация
output_ids = model.generate(input_ids=input_ids, generation_config=generation_config)[0]
output_text = tokenizer.decode(output_ids, skip_special_tokens=True)
print(output_text)
