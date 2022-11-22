# Database interface
import pdb
import sqlite3
import unittest

class Queries:
	# Initialization of tables
	INIT_TAGS = "CREATE TABLE IF NOT EXISTS tags (tagname PRIMARY KEY);"
	INIT_FILES = "CREATE TABLE IF NOT EXISTS files (filepath PRIMARY KEY);"
	INIT_FILE_TAGS = "CREATE TABLE IF NOT EXISTS filetags (tag INTEGER, file INTEGER);"

	ADD_TAG = "INSERT INTO tags (tagname) VALUES (?)"
	REM_TAG = "DELETE FROM tags WHERE tagname = ?"
	GET_TAGS = "SELECT rowid, * FROM tags"
	GET_TAG = "SELECT rowid FROM tags where tagname = ?"

	ADD_FILE = "INSERT INTO files (filepath) VALUES (?)"
	REM_FILE = "DELETE FROM files WHERE filepath = ?"
	GET_FILES = "SELECT rowid, * FROM files"
	GET_FILE = "SELECT rowid FROM files where filepath = ?"

	ADD_LINK = "INSERT INTO filetags (tag, file) VALUES (?, ?)"
	REM_LINK = "DELETE FROM filetags WHERE tag = ? OR file = ?"
	GET_LINK = "SELECT * FROM filetags WHERE tag = ? OR file = ?"

class DataBase:
	def __init__(self, db_file):
		self.con = sqlite3.connect(db_file)
		self.con.execute(
			Queries.INIT_TAGS,
		)
		self.con.execute(
			Queries.INIT_FILES,
		)
		self.con.execute(
			Queries.INIT_FILE_TAGS,
		)

	def __del__(self):
		self.con.close()

	def get_tags(self):
		return self.con.execute(Queries.GET_TAGS)

	def get_files(self):
		return self.con.execute(Queries.GET_FILES)

	def add_tag(self, tag):
		return self.con.execute(Queries.ADD_TAG, [(tag)])

	def add_file(self, file):
		return self.con.execute(Queries.ADD_FILE, [(file)])

	def get_tag(self, tag):
		res = self.con.execute(Queries.GET_TAG, [(tag)]).fetchall()

		if len(res) == 0:
			return None
		elif len (res) > 1:
			raise Exception("Duplicate tag in SQL DB")
		else:
			return res[0][0]


	def get_file(self, file):
		res = self.con.execute(Queries.GET_FILE, [(file)]).fetchall()
		if len(res) == 0:
				return None
		elif len (res) > 1:
			raise Exception("Duplicate file in SQL DB")
		else:
			return res[0][0]

	def rem_tag(self, tag):
		tag_id = self.get_tag(tag)

		if tag_id == None:
			raise Exception("rem_tag(): tag does not exist")


		return (
			self.con.execute(Queries.REM_TAG, [(tag)]),
			self.con.execute(Queries.REM_LINK, [tag_id, None]),
		)

	def rem_file (self, file):
		file_id = self.get_file(file)

		if file_id == None:
			raise Exception("rem_file(): file does not exist")

		return (
			self.con.execute(Queries.REM_FILE, [(file)]),
			self.con.execute(Queries.REM_LINK, [None, file_id]),
		)

	def add_link(self, tag_id=None, file_id=None):
		if tag_id is None and file_id is None:
			raise Exception("'tag_id' and 'file_id' cannot both be empty")

		return self.con.execute(Queries.ADD_LINK, [tag_id, file_id])

	def rem_link(self, tag_id=None, file_id=None):
		if tag_id is None and file_id is None:
			raise Exception("'tag_id' and 'file_id' cannot both be empty")
		return self.con.execute(Queries.REM_LINK, [tag_id, file_id])

	def get_link(self, tag_id=None, file_id=None):
		if tag_id is None and file_id is None:
			raise Exception("'tag_id' and 'file_id' cannot both be empty")
		return self.con.execute(Queries.GET_LINK, [tag_id, file_id])

	def close(self):
		del self

# if __name__ == "__main__":
# 	import pdb
# 	pdb.set_trace()

class DatabaseTest(unittest.TestCase):
	def test_init(self):
		db = DataBase("test.db")
		db.close()

	def test_tag(self):
		db = DataBase("test.db")
		db.add_tag("test_tag")
		tags = db.get_tags().fetchall()
		self.assertTrue(db.get_tag("test_tag") == 1)
		db.close()

	def test_file(self):
		db = DataBase("test.db")
		db.add_file("test_file")
		files = db.get_files().fetchall()
		self.assertTrue(db.get_file("test_file") == 1)
		db.close()

	def test_file_tag(self):
		db = DataBase("test.db")
		db.add_file("test_file")
		db.add_tag("test_tag")

		tags = db.get_tags().fetchall()
		files = db.get_files().fetchall()
		db.add_link(tags[0][0], files[0][0])
		l = db.get_link(tag_id=1).fetchall()
		self.assertTrue(len(l) == 1)

		ret = db.rem_file("test_file")
		tag_id = db.get_tag("test_tag")
		#pdb.set_trace()
		self.assertTrue(len(db.get_link(tag_id=tag_id).fetchall()) == 0)
		db.rem_tag("test_tag")

		db.close()


if __name__ == '__main__':
	import os
	unittest.main()
	os.remove("test.db")