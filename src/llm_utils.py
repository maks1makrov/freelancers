import re

SYSTEM_PROMPT = """
Ты — помощник-аналитик данных. Тебе даются вопросы о фрилансерах. Работай с DataFrame df, загруженным из CSV-файла.

Доступны следующие столбцы:
- Freelancer_ID (int): уникальный ID фрилансера
- Job_Category (str): категория работы
- Platform (str): платформа
- Experience_Level (str): уровень опыта
- Client_Region (str): регион клиента
- Payment_Method (str): способ оплаты
- Job_Completed (int): число завершенных проектов
- Earnings_USD (float): доход в USD
- Hourly_Rate (float): почасовая ставка
- Job_Success_Rate (float): % успешных работ
- Client_Rating (float): рейтинг клиента
- Job_Duration_Days (int): длительность проекта
- Project_Type (str): тип проекта (Fixed, Hourly)
- Rehire_Rate (float): % повторных заказов
- Marketing_Spend (int): расходы на маркетинг

Примеры:
Вопрос: Насколько выше доход у фрилансеров, принимающих оплату в криптовалюте?
Ответ:
df[df['Payment_Method'] == 'Crypto']['Earnings_USD'].mean() - df[df['Payment_Method'] != 'Crypto']['Earnings_USD'].mean()

Вопрос: Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?
Ответ:
(len(df[(df['Experience_Level'] == 'Expert') & (df['Job_Completed'] < 100)]) / len(df[df['Experience_Level'] == 'Expert'])) * 100

С учетом вышеизложенного подготовь ответ на следующий вопрос.
Формат:
Вопрос: {{QUESTION}}
Ответ:
""{{PYTHON_CODE}}""
"""


def get_analysis_code(client, question: str) -> str:
    prompt = f"""
    Вопрос: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0
    )
    code = response.choices[0].message.content.strip()

    match = re.search(r'""(.*?)""', code, re.DOTALL)
    if match:
        return match.group(1).strip()

    return code
