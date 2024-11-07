first_words = [
    "выведи",
    "озвучь"
]

second_words = [
    "колонну",
    "строку"
]


# request example: озвучь колонну balance из таблицы users где balance > 10
def check_sql(text):
    words = text.lower().split()
    if words[0] not in first_words:
        return False

    if words[1] not in second_words:
        ...


def reoginize_phrase(text):
    ...