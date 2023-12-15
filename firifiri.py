import random, logging, telebot
from telebot import types
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

API_TOKEN = '6259573339:AAECdYJSGJETtWkfnds2ZOVGZWLMyz2o3Ts'
MODEL = "microsoft/DialoGPT-medium"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

bot = telebot.TeleBot(API_TOKEN)

dialog_history = {}
user_id = 0

@bot.message_handler(commands=['start'])
def start(message):
    global user_id
    user_id - message.from_user.id
    markup_items = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton('Asuka', callback_data='asuka')
    item2 = types.InlineKeyboardButton('Zero Two',callback_data='zero_two')
    item3 = types.InlineKeyboardButton('Ryuko Matoi', callback_data='ryuoko_matoi')
    markup_items.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Choose one of the girls:', reply_markup=markup_items)

@bot.callback_query_handler(func=lambda call: True)
def but(call):
    global user_id
    if call.message:
        if call.data == 'asuka':
            bot.send_message(call.message.chat.id, 'Your choice: Asuka')
        elif call.data == 'zero_two':
            bot.send_message(call.message.chat.id, 'Your choice: Zero Two')
        elif call.data == 'ryuoko_matoi':
            bot.send_message(call.message.chat.id, 'Your choice: Ryuoko Matoi')
    markup_buttons = types.InlineKeyboardMarkup(row_width=3)
    but1 = types.InlineKeyboardButton('Friendly', callback_data='friendly')
    but2 = types.InlineKeyboardButton('Aggressive', callback_data='aggressive')
    but3 = types.InlineKeyboardButton('Mysterious', callback_data='mysterious')
    markup_buttons.add(but1, but2, but3)
    bot.send_message(call.message.chat.id, 'Choose a behaviour:', reply_markup=markup_buttons)
bot.callback_query_handler(func=lambda call: True)
def item(call):
    global user_id
    if call.message:
        if call.data == 'friendly':
            bot.send_message(call.message.chat.id, 'Chosen behaviour: Friendly')
        elif call.data == 'aggressive':
            bot.send_message(call.message.chat.id, 'Chosen behaviour: Aggressive')
        elif call.data == 'mysterious':
            bot.send_message(cal.message.chat.id, 'Chosen behaviour: Mysterious')

    bot.send_message(call.message.chat.id, 'Start chatting. Enter your message')

@bot.message_handler(func=lambda message: True)
def chat(message):
    inputs = tokenizer.encode(message.text, return_tensors='pt', truncation=True, max_length=1024)
    reply_ids = model.generate(inputs, max_length=1024, pad_token_id=tokenizer.eos_token_id, no_repeat_ngram_size=3, do_sample=True, temperature=0.7)
    reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['clear'])
def cancel(message):
    bot.send_message(message.chat.id, 'Goodbye! Feel free to start a new conversation anytime.')

bot.infinity_polling()
