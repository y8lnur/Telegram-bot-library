import config
import logging
import telebot
import json
import asyncio
from telebot import types

from db import BOOK

bot = telebot.TeleBot(config.TOKEN);


db = BOOK('books.db')


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
 
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/search")
    item2 = types.KeyboardButton("/insert")
    markup.add(item1, item2)
 
    bot.send_message(message.chat.id, "САЛАМ, {0.first_name}!\nМен Қазақ Әдебиет базасының ботымын\nҚазақ әдебиетіндегі шығармаларды іздеймін\nБастаймызба?".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)



@bot.message_handler(commands=['search'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Автор бойынша")
	item2 = types.KeyboardButton("Жанр бойынша")
	item3 = types.KeyboardButton("Шығарма аты бойынша")
	markup.add(item1, item2, item3)
	bot.send_message(message.chat.id, "Шығарманы қандай параметр бойынша іздейміз?", reply_markup=markup)
	bot.register_next_step_handler(message, choice);

	
def choice(message):
	if message.text == "Жанр бойынша":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("роман")
		item2 = types.KeyboardButton("тарихи")
		markup.add(item1, item2)
		bot.send_message(message.chat.id, 'Жанрды таңдауыңызды сұраймын', reply_markup=markup)
		bot.register_next_step_handler(message, out_genre);
	elif message.text == "Автор бойынша":
		a = telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.from_user.id, "{0.first_name}, сізден Автор есімін жазуыңызды сұрауға мәжбүрмін".format(message.from_user), reply_markup = a);
		bot.register_next_step_handler(message, out_author);
	elif message.text == "Шығарма аты бойынша":
		a = telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.from_user.id, "{0.first_name}, сізден шығарма атын жазуыңызды сұрауға мәжбүрмін".format(message.from_user), reply_markup = a);
		bot.register_next_step_handler(message, out_name);	
	elif message.text == "/insert":
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item1 = types.KeyboardButton("Енгіземіз")
		markup.add(item1)
		bot.send_message(message.chat.id, "Деректер енгіземіз бе?", reply_markup = markup)
		bot.register_next_step_handler(message, insert);
	elif message.text == "/search":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Автор бойынша")
		item2 = types.KeyboardButton("Жанр бойынша")
		item3 = types.KeyboardButton("Шығарма аты бойынша")
		markup.add(item1, item2, item3)
		bot.send_message(message.chat.id, "Шығарманы қандай параметр бойынша іздейміз?", reply_markup=markup)
		bot.register_next_step_handler(message, choice);
	else:
		bot.send_message(message.chat.id, "Қымбатты {0.first_name}, мен сізді түсінбедім.\n/start теріңіз".format(message.from_user))	

def out_genre(message): 
    global genre;
    genre = message.text;
    res = db.search_genre(genre)
    if (db.genre_exists(message.text) == True):
    	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    	item1 = types.KeyboardButton("Автор бойынша")
    	item2 = types.KeyboardButton("Жанр бойынша")
    	item3 = types.KeyboardButton("Шығарма аты бойынша")
    	markup.add(item1, item2, item3)
    	for x in res:
    		bot.send_message(message.from_user.id, f'Шығарма атауы: {x[0]}\nАвтор есімі: {x[1]}\nШығарма жанры: {x[2]}\nШыққан жылы: {x[3]}\nҚысқаша сипаттамасы:{x[4]}' );
    	bot.send_message(message.from_user.id,'Тағы іздеу үшін батырмаға басыңыз', reply_markup = markup)
    	bot.register_next_step_handler(message, choice);
    elif message.text == "/search":
    	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    	item1 = types.KeyboardButton("Автор бойынша")
    	item2 = types.KeyboardButton("Жанр бойынша")
    	item3 = types.KeyboardButton("Шығарма аты бойынша")
    	markup.add(item1, item2, item3)
    	bot.send_message(message.chat.id, "Шығарманы қандай параметр бойынша іздейміз?", reply_markup=markup)
    	bot.register_next_step_handler(message, choice);
    elif genre == "/insert":
    	a = telebot.types.ReplyKeyboardRemove()
    	bot.send_message(message.from_user.id, reply_markup = a);
    	bot.register_next_step_handler(message, inStart);
    else:
    	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    	item1 = types.KeyboardButton("Автор бойынша")
    	item2 = types.KeyboardButton("Жанр бойынша")
    	item3 = types.KeyboardButton("Шығарма аты бойынша")
    	markup.add(item1, item2, item3)
    	bot.send_message(message.from_user.id, '{0} - жанры бойынша біздің базамызда шығарма жоқ.\nОны қосқыңыз келсе /insert командасын қолдану мүмкіндігіңіз бар.'.format(message.text));
    	bot.send_message(message.from_user.id,'Тағы іздеу үшін батырмаға басыңыз', reply_markup = markup)
    	bot.register_next_step_handler(message, choice);
def out_author(message):
	global author;
	author = message.text;
	res = db.search_author(author)
	if (db.author_exists(message.text) == True):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Автор бойынша")
		item2 = types.KeyboardButton("Жанр бойынша")
		item3 = types.KeyboardButton("Шығарма аты бойынша")
		markup.add(item1, item2, item3)
		for x in res:
			bot.send_message(message.from_user.id, f'Шығарма атауы: {x[0]}\nАвтор есімі: {x[1]}\nШығарма жанры: {x[2]}\nШыққан жылы: {x[3]}\nҚысқаша сипаттамасы:{x[4]}' );
		bot.send_message(message.from_user.id,'Тағы іздеу үшін батырмаға басыңыз', reply_markup = markup)
		bot.register_next_step_handler(message, choice);
	elif message.text == "/search":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Автор бойынша")
		item2 = types.KeyboardButton("Жанр бойынша")
		item3 = types.KeyboardButton("Шығарма аты бойынша")
		markup.add(item1, item2, item3)
		bot.send_message(message.chat.id, "Шығарманы қандай параметр бойынша іздейміз?", reply_markup=markup)
		bot.register_next_step_handler(message, choice);
	elif message.text == "/insert":
		a = telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.from_user.id, reply_markup = a);
		bot.register_next_step_handler(message, inStart);
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Автор бойынша")
		item2 = types.KeyboardButton("Жанр бойынша")
		item3 = types.KeyboardButton("Шығарма аты бойынша")
		markup.add(item1, item2, item3)
		bot.send_message(message.from_user.id, '{0} - авторының шығармалары біздің базамызда жоқ.\nОны қосқыңыз келсе /insert командасын қолдану мүмкіндігіңіз бар.'.format(message.text));
		bot.send_message(message.from_user.id,'Тағы іздеу үшін батырмаға басыңыз', reply_markup = markup)
		bot.register_next_step_handler(message, choice);		
def out_name(message):
	global name;
	name = message.text;
	res = db.search_name(name)
	if (db.name_exists(message.text) == True):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Автор бойынша")
		item2 = types.KeyboardButton("Жанр бойынша")
		item3 = types.KeyboardButton("Шығарма аты бойынша")
		markup.add(item1, item2, item3)
		for x in res:
			bot.send_message(message.from_user.id, f'Шығарма атауы: {x[0]}\nАвтор есімі: {x[1]}\nШығарма жанры: {x[2]}\nШыққан жылы: {x[3]}\nҚысқаша сипаттамасы:{x[4]}' );
		bot.send_message(message.from_user.id,'Тағы іздеу үшін батырмаға басыңыз', reply_markup = markup)
		bot.register_next_step_handler(message, choice)
	elif message.text == "/search":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Автор бойынша")
		item2 = types.KeyboardButton("Жанр бойынша")
		item3 = types.KeyboardButton("Шығарма аты бойынша")
		markup.add(item1, item2, item3)
		bot.send_message(message.chat.id, "Шығарманы қандай параметр бойынша іздейміз?", reply_markup=markup)
		bot.register_next_step_handler(message, choice);
		
	elif message.text == "/insert":
		a = telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.from_user.id, reply_markup = a);
		bot.register_next_step_handler(message, inStart);	
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Автор бойынша")
		item2 = types.KeyboardButton("Жанр бойынша")
		item3 = types.KeyboardButton("Шығарма аты бойынша")
		markup.add(item1, item2, item3)
		bot.send_message(message.from_user.id, '{0} - шығармасы біздің базамызда жоқ.\nОны қосқыңыз келсе /insert командасын қолдану мүмкіндігіңіз бар.'.format(message.text));
		bot.send_message(message.from_user.id,'Тағы іздеу үшін батырмаға басыңыз', reply_markup = markup)
		bot.register_next_step_handler(message, choice);
@bot.message_handler(commands=['insertauthor'])

def inStarta(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = types.KeyboardButton("Енгіземіз")
	markup.add(item1)
	bot.send_message(message.chat.id, "Деректер енгіземіз бе?", reply_markup = markup)
	bot.register_next_step_handler(message, insert);
def ininfoa(message):
	
	if qaqa == 0:
		authorinfo = message.text
		db.add_author(author_name, author_info)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Енгіземіз")
		item2 = types.KeyboardButton("Жоқ, шығу")
		markup.add(item1, item2)
		bot.send_message(message.chat.id, "Деректер сәтті қосылды\nТағы енгіземіз бе?", reply_markup = markup)
		bot.register_next_step_handler(message, insert)
def inname(message):
	if message.text == "/search":
		bot.register_next_step_handler(message, start)
	elif message.text == "/insert":
		bot.register_next_step_handler(message, inStarta)
	else:
		global authorname
		authorname = message.text
		bot.send_message(message.chat.id, "автор жайлы ақпарат")
		if db.name_exists(name) == False:
			bot.register_next_step_handler(message, ininfoa)
			return authorname
		else:
			bot.send_message(message.chat.id, "Бұл шығарма базада бар")

def insert(message):
	if message.text == "Енгіземіз":
		a = telebot.types.ReplyKeyboardRemove()
		qaqa = 0
		bot.register_next_step_handler(message, inname)
		bot.send_message(message.chat.id, "Автор есімі", reply_markup = a)
		return qaqa
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("/search")
		item2 = types.KeyboardButton("/insert")
		markup.add(item1, item2)
		bot.send_message(message.chat.id, "Ал,{0.first_name} енді не істейміз?".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)
		if message.text == "/search":
			bot.register_next_step_handler(message, start)
		elif message.text == "/insert":
			bot.register_next_step_handler(message, inStart)
	
@bot.message_handler(commands=['insert'])		
def inStart(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = types.KeyboardButton("Енгіземіз")
	markup.add(item1)
	bot.send_message(message.chat.id, "Деректер енгіземіз бе?", reply_markup = markup)
	bot.register_next_step_handler(message, insert);
def inshort_desc(message):
	if qaq == 1:
		short_desc = message.text
		db.add_book_admin(name, author, genre, year, short_desc)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Tuh-_-MawroH667")
		item2 = types.KeyboardButton("Жоқ, шығу")
		markup.add(item1, item2)
		bot.send_message(message.chat.id, "Деректер сәтті қосылды\nТағы енгіземіз бе?", reply_markup = markup)
		bot.register_next_step_handler(message, insert)
	elif qaq == 0:
		short_desc = message.text
		db.add_book_user(name, author, genre, year, short_desc, message.from_user.id, message.from_user.first_name)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Енгіземіз")
		item2 = types.KeyboardButton("Жоқ, шығу")
		markup.add(item1, item2)
		bot.send_message(message.chat.id, "Деректер сәтті қосылды\nТағы енгіземіз бе?", reply_markup = markup)
		bot.register_next_step_handler(message, insert)
def inyear(message):
	if message.text == "/search":
		bot.register_next_step_handler(message, start)
	elif message.text == "/insert":
		bot.register_next_step_handler(message, inStart)
	else:
		global short_desc
		global year
		year = message.text
		bot.send_message(message.chat.id, "Шығарманың қысқаша сипаттамасы")
		bot.register_next_step_handler(message, inshort_desc)
		return year
def ingenre(message):
	if message.text == "/search":
		bot.register_next_step_handler(message, start)
	elif message.text == "/insert":
		bot.register_next_step_handler(message, inStart)
	else:
		a = telebot.types.ReplyKeyboardRemove()
		global genre
		genre = message.text
		bot.send_message(message.chat.id, "жыл", reply_markup = a)
		bot.register_next_step_handler(message, inyear)
		return genre

def inauthor(message):
	if message.text == "/search":
		bot.register_next_step_handler(message, start)
	elif message.text == "/insert":
		bot.register_next_step_handler(message, inStart)
	else:
		global author
		author = message.text
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("тарихи")
		item2 = types.KeyboardButton("роман")
		markup.add(item1, item2)
		bot.send_message(message.chat.id, "жанр\nберілген жанрлар арасында болмаса өзіңіз тере аласыз", reply_markup = markup)

		bot.register_next_step_handler(message, ingenre)
		return author

def inname(message):
	if message.text == "/search":
		bot.register_next_step_handler(message, start)
	elif message.text == "/insert":
		bot.register_next_step_handler(message, inStart)
	else:
		global name
		name = message.text
		bot.send_message(message.chat.id, "автор")
		if db.name_exists(name) == False:
			bot.register_next_step_handler(message, inauthor)
			return name
		else:
			bot.send_message(message.chat.id, "Бұл шығарма базада бар")

def insert(message):
	if message.text == "Tuh-_-MawroH667":
		global qaq 
		qaq = 1
		a = telebot.types.ReplyKeyboardRemove()
		bot.register_next_step_handler(message, inname)
		bot.send_message(message.chat.id, "Кітап аты", reply_markup = a)
		return qaq
	elif message.text == "Енгіземіз":
		a = telebot.types.ReplyKeyboardRemove()
		qaq = 0
		bot.register_next_step_handler(message, inname)
		bot.send_message(message.chat.id, "Шығарма атауы", reply_markup = a)
		return qaq
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("/search")
		item2 = types.KeyboardButton("/insert")
		markup.add(item1, item2)
		bot.send_message(message.chat.id, "Ал,{0.first_name} енді не істейміз?".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)
		if message.text == "/search":
			bot.register_next_step_handler(message, start)
		elif message.text == "/insert":
			bot.register_next_step_handler(message, inStart)
	
bot.polling(none_stop=True)