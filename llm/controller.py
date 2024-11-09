from rabbit_worker import RabbitWorker
from service import LLMService


class LLMController:
    def __init__(self):
        self.worker = RabbitWorker(on_message_callback=self.on_message)
        self.service = LLMService()

    def run(self):
        self.worker.run()

    def prepare_prompt(self, request) -> str:
        return "В чем смысл жизни?"

    def on_message(self, ch, method, properties, body):
        prompt = self.prepare_prompt(body)
        result = self.service.generate(prompt)
        self.worker.answer(result)


if __name__ == "__main__":
    controller = LLMController()
    controller.run()

