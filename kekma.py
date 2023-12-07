import random
import telebot
from telebot import types
from transformers import AutoModelForCausalLM, AutoTokenizer

API_TOKEN = '6259573339:AAECdYJSGJETtWkfnds2ZOVGZWLMyz2o3Ts'
MODEL = "microsoft/DialoGPT-medium"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

bot = telebot.TeleBot(API_TOKEN)

personas = {
    'Asuka': ['persona1', 'persona2'],
    'Zero Two': ['persona1', 'persona2'],
    'Ryuko Matoi': ['persona1', 'persona2'],
}

behaviors = {
    'Friendly': ['friendly_behavior1', 'friendly_behavior2'],
    'Aggressive': ['aggressive_behavior1', 'aggressive_behavior2'],
    'Mysterious': ['mysterious_behavior1', 'mysterious_behavior2'],
}

dialog_history = {}

@bot.message_handler(commands=['start'])
def start(message):
    #reply_keyboard = [['Asuka'], ['Zero Two'], ['Ryuko Matoi']]
    markup = types.InlineKeyboardMarkup()
    #markup = types.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    item1 = types.InlineKeyboardButton('Asuka', callback_data='asuka')
    item2 = types.InlineKeyboardButton('Zero Two',callback_data='zero_two')
    item3 = types.InlineKeyboardButton('Ryuko Matoi', callback_data='ryuoko_matoi')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Choose one of the girls:', reply_markup=markup)
    bot.register_next_step_handler(message, chosen_persona)

def chosen_persona(message):
    user_id = message.from_user.id
    dialog_history[user_id] = {'chosen_girl': message.text, 'messages': []}
    reply_keyboard = [['Friendly'], ['Aggressive'], ['Mysterious']]
    markup = types.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    bot.send_message(message.chat.id, 'Choose a behaviour:', reply_markup=markup)
    bot.register_next_step_handler(message, chosen_behaviour)

def chosen_behaviour(message):
    user_id = message.from_user.id
    dialog_history[user_id]['chosen_behaviour'] = message.text
    bot.send_message(message.chat.id, 'Start chatting:')
    bot.register_next_step_handler(message, chat)

def chat(message):
    user_id = message.from_user.id
    user_data = dialog_history.get(user_id, None)
    if user_data is None:
        bot.send_message(message.chat.id, "An error occurred. Please /start again.")
        return
    persona = random.choice(personas[user_data['chosen_girl']])
    behavior = random.choice(behaviors[user_data['chosen_behaviour']])
    user_data['messages'].append(message.text)
    dialog_str = f"{persona} {tokenizer.eos_token} {behavior} {' '.join(user_data['messages'])}"
    # Используем 'pt' для PyTorch как backend
    inputs = tokenizer.encode(dialog_str, return_tensors='pt', truncation=True, max_length=1024)
    reply_ids = model.generate(inputs, max_length=1024, pad_token_id=tokenizer.eos_token_id, no_repeat_ngram_size=3, do_sample=True, temperature=0.7)
    reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    user_data['messages'].append(reply)
    user_data['messages'] = user_data['messages'][-10:]
    reply = reply[:4096] if len(reply) > 4096 else reply
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['cancel'])
def cancel(message):
    dialog_history.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, 'Goodbye! Feel free to start a new conversation anytime.')

bot.infinity_polling()