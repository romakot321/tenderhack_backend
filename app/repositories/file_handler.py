import os
from app.models.dtos import File
import textract
from docx.api import Document
import mimetypes
import requests


class FileHandler:

    def __is_task_desciption_document(self, path):
        KEYWORDS = [
            'тз',
            'техническое задание',
            'техническое_задание',
            'техническое-задание',
        ]
        filename = os.path.basename(path).lower()
        for keyword in KEYWORDS:
            if keyword in filename:
                return True
        return False

    def __is_contract_document(self, path):
        KEYWORDS = [
            'контракт',
            'договор',
        ]
        filename = os.path.basename(path).lower()
        for keyword in KEYWORDS:
            if keyword in filename:
                return True
        return False

    def __file_docx_to_txt(self, path: str):
        return textract.process(path).decode('utf-8')

    def __file_doc_to_txt(self, path: str):
        return textract.process(path).decode('utf-8')

    def __file_pdf_to_txt(self, path: str):
        return textract.process(path).decode('utf-8')

    def __optimize_text(self, text):
        while ("\n\n" in text):
            text = text.replace("\n\n", "\n")
        return text

    def __extract_tables_docx(self, path):
        document = Document(path)
        if len(document.tables) == 0:
            return None
        else:
            tables = []
            for table in document.tables:
                table_data = []
                keys = None
                for i, row in enumerate(table.rows):
                    text = (cell.text for cell in row.cells)
                    if i == 0:
                        keys = tuple(text)
                        continue
                    row_data = dict(zip(keys, text))
                    table_data.append(row_data)
                tables.append(table_data)
            return tables


    def __extract_tables(self, path):
        tables = []
        if path[-5:] == ".docx":
            tables = self.__extract_tables_docx(path)
        return tables

    def __file_to_text(self, path: str):
        text = ""
        if path[-4:] == ".pdf":
            text = self.__file_pdf_to_txt(path)
        elif path[-4:] == ".doc":
            text = self.__file_doc_to_txt(path)
        elif path[-5:] == ".docx":
            text = self.__file_docx_to_txt(path)

        text = self.__optimize_text(text)
        return text

    def __download_file(self, file_id):
        url = "https://zakupki.mos.ru/newapi/api/FileStorage/Download?id=" + file_id
        try:
            query = requests.get(url)
            content_type = query.headers['Content-Type']
            file_extension = mimetypes.guess_extension(content_type.split(';')[0])
            output_path = "./assets/session_file"+file_id+file_extension

            response = requests.get(url)
            with open(output_path, 'wb') as file:
                file.write(response.content)
            return output_path
        except:
            print("Error: unable to download file via file_id", file_id)
            return None


    def __delete_file(self, path):
        os.remove(path)

    def __save_txt_file(self, file_id, text):
        path = "./assets/text_file"+file_id+".txt"
        with open(path, 'w') as file:
            file.write(text)

    def handle_file(self, file_id):
        path_text_file = "./assets/text_file"+file_id+".txt"
        if os.path.exists(path_text_file):
            text = open(path_text_file, 'r').read()
            result = File(text=text)
            return result
        else:
            path = self.__download_file(file_id)
            if path is None:
                return None
            text = self.__file_to_text(path)
            self.__save_txt_file(file_id, text)
            result = File(
                text=text
            )
            result.is_TZ = self.__is_task_desciption_document(path)
            self.__delete_file(path)
            return result



