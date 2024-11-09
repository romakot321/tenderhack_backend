from transformers import AutoTokenizer, AutoModelForCausalLM


class LLMService:
    model_name = "Vikhrmodels/Vikhr-Qwen-2.5-0.5B-Instruct"
    system_prompt = "Вы - pipipu, помощник с искусственным интеллектом, созданный Котом, чтобы быть полезным, безобидным и честным."

    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def generate(self, prompt: str):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]
        input_ids = self.tokenizer.apply_chat_template(messages, truncation=True, return_tensors="pt")
        output = self.model.generate(
            input_ids,
            max_new_tokens=128,
            temperature=0.3,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    print(LLMService().generate("Как у тебя дела?"))
