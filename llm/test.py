from transformers import AutoModelForCausalLM, AutoTokenizer

# Загрузка модели и токенизатора
model_name = "Vikhrmodels/Vikhr-Qwen-2.5-0.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Подготовка входного текста
input_text = "'Совпадение названий #1НАЗВАНИЕ# #2НАЗВАНИЕ#' это абсолютное равенство слов 1НАЗВАНИЕ и 2НАЗВАНИЕ."
input_text += "Совпадение названий #Три сосиски# #ЗАПАСНЫЕ ЧАСТИ ДЛЯ ТРАНСПОРТНЫХ СРЕДСТВ#"
input_text += "Ответь только ДА или НЕТ, и укажи причину совпадения."

messages = [
    {"role": "system", "content": "Вы - pipipu, помощник с искусственным интеллектом, созданный Котом, чтобы быть полезным, безобидным и честным."},
    {"role": "user", "content": input_text},
]

# Токенизация и генерация текста
input_ids = tokenizer.apply_chat_template(messages, truncation=True, return_tensors="pt")
output = model.generate(
    input_ids,
    max_new_tokens=256,
    temperature=0.32,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    top_k=50,
    top_p=0.95,
)

# Декодирование и вывод результата
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Answer: ", generated_text)

