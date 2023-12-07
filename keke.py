import telebot
from transformers import AutoModelForCausalLM, AutoTokenizer

# Загружаем языковую модель и токенизатор
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

bot = telebot.TeleBot("6259573339:AAECdYJSGJETtWkfnds2ZOVGZWLMyz2o3Ts")

# Список виртуальных подруг
friends = ["Sakura", "Asuna", "Zero Two"]

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я виртуальная подруга. Выбери одну из персонажек: Sakura, Asuna или Zero Two")

# Обработчик для текстовых сообщений
@bot.message_handler(func=lambda msg: True)
def chat(message):
    user_message = message.text
    friend = ""  # Переменная для хранения выбранной подруги

    # Проверяем, выбрал ли пользователь персонажа
    if user_message.lower() in map(str.lower, friends):
        friend = user_message
        bot.reply_to(message, f"Ты выбрал {friend}. Привет, я твоя виртуальная подруга {friend}! Чем могу помочь?")
    elif friend != "":
        # Находим индекс выбранной подруги
        friend_index = friends.index(friend)

        # Используем DialoGPT для генерации ответа
        input = tokenizer.encode(f"USER: {user_message} FRIEND: {friend}:", return_tensors="pt")
        output = model.generate(input, max_length=100, num_return_sequences=1)
        response = tokenizer.decode(output[:, input.shape[-1]:][0], skip_special_tokens=True)

        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Прости, я не знаю такого персонажа. Выбери одну из персонажек: Sakura, Asuna или Zero Two")

# Запуск бота
bot.polling()
