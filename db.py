import sqlite3

class BOOK:


	def __init__(self, database):
		self.connection = sqlite3.connect(database, check_same_thread=False)
		self.cursor = self.connection.cursor()
		conn = sqlite3.connect('books.db', check_same_thread = False)
	def search_name(self, name: str):
		with self.connection:
			return self.cursor.execute("SELECT name, author, genre, year, short_desc FROM book_list WHERE name = ?", (name, )).fetchall()
	def search_author(self, author: str):
		with self.connection:
			return self.cursor.execute("SELECT name, author, genre, year, short_desc FROM book_list WHERE author = ?", (author, )).fetchall()
	def search_genre(self, genre: str):
		with self.connection:
			return self.cursor.execute("SELECT name, author, genre, year, short_desc FROM book_list WHERE genre = ?", (genre, )).fetchall()
	def out_author(self, athor_name, author_info):
		with self.connection:
			return self.cursor.execute("SELECT author_name, author_info FROM author WHERE author_name = ?", (author, )).fetchall()
			
	def name_exists(self, name):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM book_list WHERE name = ?', (name,)).fetchall()
			return bool(len(result))

	def genre_exists(self, genre):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM book_list WHERE genre = ?', (genre,)).fetchall()
			return bool(len(result))	

	def author_exists(self, author):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM book_list WHERE author = ?', (author,)).fetchall()
			return bool(len(result))

	
	def add_book_admin(self, name: str, author: str, genre: str, year: int, short_desc: str):
		with self.connection:
			return self.cursor.execute("INSERT INTO book_list (name, author, genre, year, short_desc) VALUES(?, ?, ?, ?, ?)", (name, author, genre, year, short_desc))


	def add_book_user(self, name: str, author: str, genre: str, year: int, short_desc: str, user_id: int, user_name: str):
		with self.connection:
			return self.cursor.execute("INSERT INTO book_list_user (name, author, genre, year, short_desc, user_id, user_name) VALUES(?, ?, ?, ?, ?, ?, ?)", (name, author, genre, year, short_desc, user_id, user_name))
	def add_author(self, author_name, author_info):
		with self.connection:
			return self.cursor.execute("INSERT INTO author (author_name, author_info) VALUES(?, ?)", (author_name, author_info))
	def close(self):
		"""Закрываем соединение с БД"""
		self.connection.close()

