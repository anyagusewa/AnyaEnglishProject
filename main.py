import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
import os


#Класс для перевода слов с русского на английский через Google Translate
class Translator:
    def __init__(self):
        self.driver = uc.Chrome()

    def translate(self, word):
        self.driver.get("https://translate.google.com/")
        self.set_language("ru","en")

        input_box = self.driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Исходный текст']") #поиск поля ввода
        input_box.send_keys(word) #ввод слова в поле перевода
        time.sleep(2)

        try:
            translation = self.driver.find_element(By.CSS_SELECTOR, "span[jsname='W297wb']").text
        except:
            translation = "Не удалось получить перевод"

        return translation

    #Парсит 10 примеров предложений с Reverso Context
    def get_examples(self, word):
        url = f"https://context.reverso.net/translation/russian-english/{word}"
        self.driver.get(url)
        time.sleep(3)

        examples = []

        try:
            en_sentences = self.driver.find_elements(By.CSS_SELECTOR, "div.trg.ltr")[:10]
            ru_sentences = self.driver.find_elements(By.CSS_SELECTOR,"div.src.ltr")[:10]

            for en, ru in zip(en_sentences,ru_sentences):
                examples.append((en.text, ru.text)) #добавляем в список кортеж из пары предложений

        except Exception as e:
            print("Ошибка парсинга примеров:", e)

        return examples


    def close(self):
        self.driver.quit()


    def set_language(self,source_lang, target_lang):
        self.driver.get(f"https://translate.google.com/?sl={source_lang}&tl={target_lang}")
        time.sleep(2)

# Функция для сохранения в текстовый файл
def save_to_txt(word, translation, examples, filename ='translations.txt'):
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", encoding="utf-8") as file:
        if not file_exists:
            file.write("=== Словарь переводов ===\n\n")

        file.write(f"Слово: {word}\n")
        file.write(f"Перевод: {translation}\n")
        file.write("Примеры предложений:\n")

        for i, (en, ru) in enumerate(examples, 1):
            file.write(f"{i}. {en} → {ru}\n")

        file.write("\n" + "=" * 40 + "\n\n")

    print(f"✅ Данные сохранены в {filename}!")


if __name__ == "__main__":

    translator = Translator()
    user_word = input("Введите слово на русском: ")

    translation = translator.translate(user_word)
    print(f"Перевод: {translation}")

    examples = translator.get_examples(user_word)
    print("Примеры предложений:")
    for i, (en, ru) in enumerate(examples, 1):
        print(f"{i}. {en} → {ru}")

    save_to_txt(user_word, translation, examples)

    translator.close()