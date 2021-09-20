import sqlite3

class Database:

    def __init__(self,db):
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute("create table if not exists book(id INTEGER PRIMARY KEY, title text,author text,year integer, isbn integer)")
        conn.commit()
        conn.close()

    def insert(title, author,year,isbn):
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("insert into book values(NULL,?,?,?,?)",(title, author,year,isbn))
        conn.commit()
        conn.close()

    def view():
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("select * from book")
        rows=cur.fetchall()
        conn.close()
        return rows

    def search(title="", author="",year="",isbn=""):
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("select * from book where title=? or author=? or year=? or isbn=?",(title, author,year,isbn))
        rows=cur.fetchall()
        conn.close()
        return rows

    def delete(id):
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("delete from book where id=?",(id,))#dont forget the comma
        conn.commit()
        conn.close()

    def update(id, title,author,year,isbn):
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("update book set title=?,author=?,year=?,isbn=? where id=?",(title,author,year,isbn,id))
        conn.commit()
        conn.close()


