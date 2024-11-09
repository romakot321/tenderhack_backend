from transformers import AutoTokenizer, AutoModelForCausalLM


class LLMService:
    model_name = "ai-forever/rugpt3large_based_on_gpt2"
    system_prompt = "Вы - pipipu, помощник с искусственным интеллектом, созданный Котом, чтобы быть полезным, безобидным и честным."

    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def generate(self, prompt: str):
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
        output = self.model.generate(
            input_ids,
            max_length=100,
            num_return_sequences=3,
            top_p=0.9,
            do_sample=True,
            num_beams=5,
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    print(LLMService().generate("Как у тебя дела?"))
