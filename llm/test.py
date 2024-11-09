from transformers import AutoModelForCausalLM, AutoTokenizer

# Загрузка модели и токенизатора
model_name = "ai-forever/rugpt3large_based_on_gpt2"
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
#input_ids = tokenizer.apply_chat_template(messages, truncation=True, return_tensors="pt")
while True:
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(
        input_ids,
        max_length=100,
        num_return_sequences=3,
        top_p=0.9,
        do_sample=True,
        num_beams=5,
    )

# Декодирование и вывод результата
    for generated in output:
        text = tokenizer.decode(generated, skip_special_tokens=True)
        print("Answer: ", text)

