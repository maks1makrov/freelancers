from llm_utils import get_analysis_code

from data_utils import load_data
from openai import OpenAI
from dotenv import load_dotenv
import os


def main():
    try:
        print("Добро пожаловать!")

        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        df = load_data()

        while True:
            question = input("\nВведите ваш запрос (или '7' для выхода): ")

            if question == '7':
                print("Завершаю программу...")
                break

            code = get_analysis_code(client, question)

            print("\n\033[1mЗапрос:\033[0m", question)
            print("\033[1mСгенерированный код:\033[0m\n", code)

            local_vars = {'df': df}
            result = eval(code, {}, local_vars)

            print("\033[1mОтвет:\033[0m")
            print(f"По вашему запросу: '{question}'\n\033[91mПолучен результат: {result}\033[0m")

    except Exception as e:
        print("\033[91mОшибка выполнения запроса:\033[0m", e)


if __name__ == "__main__":
    main()
