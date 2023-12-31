import random, logging, telebot, json
from telebot import types
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

API_TOKEN = '6259573339:AAECdYJSGJETtWkfnds2ZOVGZWLMyz2o3Ts'
MODEL = "microsoft/DialoGPT-large"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

bot = telebot.TeleBot(API_TOKEN)

history = {}
user_id = 0

def dump():
    with open('kek//history.json', 'w') as hist:
        json.dump(history, hist)

def load():
    with open('kek/history.json', 'r') as hist:
        ld = json.load(hist)
    return ld

@bot.message_handler(commands=['start'])
def start(message):
    user_id - message.from_user.id
    history[user_id] = {'char': '', 'behav': '', 'hist': []}
    markup_items = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton('Asuka', callback_data='asuka')
    item2 = types.InlineKeyboardButton('Zero Two',callback_data='zero_two')
    item3 = types.InlineKeyboardButton('Ryuko Matoi', callback_data='ryuoko_matoi')
    markup_items.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Choose one of the girls:', reply_markup=markup_items)

@bot.message_handler(commands=['ls'])
def ls(message):
    bot.send_message(message.chat.id, f'{load()}')
@bot.callback_query_handler(func=lambda call: True)
def but(call):
    if call.data == 'asuka':
        history[user_id]['char'] = 'Asuka'
        bot.send_message(call.message.chat.id, 'Your choice: Asuka')
    elif call.data == 'zero_two':
        history[user_id]['char'] = 'Zero Two'
        bot.send_message(call.message.chat.id, 'Your choice: Zero Two')
    elif call.data == 'ryuoko_matoi':
        history[user_id]['char'] = 'Ryouko Matoi'
        bot.send_message(call.message.chat.id, 'Your choice: Ryuoko Matoi')
    dump()
    bot.send_message(call.message.chat.id, 'Start chating')

@bot.message_handler(func=lambda message: True)
def chat(message):
    #inputs = tokenizer.encode(message.text, return_tensors='pt', truncation=True, max_length=1024)
    inputs = tokenizer.encode(message.text + tokenizer.eos_token, return_tensors='pt')
    reply_ids = model.generate(inputs, max_length=1024, pad_token_id=tokenizer.eos_token_id, no_repeat_ngram_size=3, do_sample=True, temperature=1.0)
    reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    bot.send_message(message.chat.id, f'{reply}')

@bot.message_handler(commands=['clear'])
def cancel(message):
    bot.send_message(message.chat.id, 'Goodbye! Feel free to start a new conversation anytime.')
bot.infinity_polling()
