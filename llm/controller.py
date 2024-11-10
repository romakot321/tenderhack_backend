from pydantic import BaseModel
import json

from rabbit_worker import RabbitWorker
from service import LLMService
from file_handler import FileHandler


_criteria_name_to_id: dict[str, str] = {
    'name': '1',
    'executor': '2',
    'license': '3',
    'delivery_schedule': '4',
    'max_cost': '5',
    'start_cost': '6',
    'task_document': '7'
}


class File(BaseModel):
    path: str
    is_TZ: bool


class Parameters(BaseModel):
    qs_id: int
    criteria: list[str]
    files: list[File]


_prompt = """
Проверь текст на соблюдение Критериев проверки.
Шаблон критерия: "НОМЕР КРИТЕРИЯ) Название критерия: пояснение"
Критерии проверки:
1) Соответствие названия: Проверьте, что название в проекте контракта точно совпадает с названием в техническом задании, если оно предоставлено.
2) Обеспечение исполнения контракта: Если в проекте контракта установлено требование по обеспечению исполнения контракта, убедитесь, что оно также указано в техническом задании (если оно имеется).
3) Сертификаты/Лицензии: Если в проекте контракта нет упоминания сертификатов или лицензий, убедитесь, что таких требований нет и в прикрепленном техническом задании. Если сертификаты или лицензии указаны, проверьте, что требуемые документы перечислены и в проекте контракта, и в техническом задании (если оно имеется).
4) График и этап поставки: Убедитесь, что значения «График поставки» и «Этап поставки» совпадают между проектом контракта и техническим заданием (если оно имеется).
5) Предельная стоимость: Если указано «Максимальное значение цены контракта», убедитесь, что значение совпадает с данными в техническом задании (если оно имеется). В противном случае, если указана «Начальная цена», убедитесь, что в техническом задании (если оно имеется) значится «Цена Контракта».
6) Соответствие спецификации для товаров: Если техническое задание предоставлено, убедитесь, что наименования и характеристики товаров в проекте контракта совпадают с указанными в техническом задании, включая количество товаров. Если в техническом задании больше характеристик, чем в проекте контракта, отметьте это для дальнейшей проверки, но не снимайте с публикации автоматически.

ПРОЙДЕНО используется для критериев, прошедших проверку, иначе используется ПРОВАЛЕНО.

Пример структуры отчета, при котором пользователь отправил номера критериев 1,2 и 5:
К1 (Соответствие названия): ПРОЙДЕНО
К2 (Обеспечение исполнения контракта): ПРОВАЛЕНО
К5 (Предельная стоимость): ПРОВАЛЕНО

Ваш ответ для каждого критерия должен быть следующим: НОМЕР КРИТЕРИЯ (Название критерия): ПРОЙДЕНО или ПРОВАЛЕНО
"""


class LLMController:
    def __init__(self):
        self.worker = RabbitWorker(on_message_callback=self.on_message)
        self.service = LLMService()
        self.file_handler = FileHandler()

    def run(self):
        self.worker.run()

    def prepare_prompt(self, files: list[File], criteria: list[str]) -> str:
        files_content = []
        for file in files:
            files_content.append(self.file_handler.read_file(file.path))
        prompt = _prompt + "\nТекст: "
        prompt += '\n\n'.join(content[0] for content in files_content) + '\n\n'
        prompt += "Ответ: "
        # prompt += ''.join([_criteria_name_to_id.get(crit, '') for crit in criteria])
        return prompt

    def on_message(self, ch, method, properties, body):
        print("Received:", body)
        body = Parameters.model_validate_json(body.decode())
        prompt = self.prepare_prompt(body.files, body.criteria)
        llm_result = self.service.generate(prompt)
        response = {
            'text': llm_result.split("<|im_start|>assistant")[1][:5000],
            'id': body.qs_id
        }
        self.worker.answer(json.dumps(response))


if __name__ == "__main__":
    controller = LLMController()
    controller.run()

