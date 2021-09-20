"""
A program that stores this book information
Title, Author
Year, ISBN
list box and slding bar

USer can:
view all records
search entry
add an entry
update entry
delete
close
"""

from tkinter import *


import sqlite3


class Database:

    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        self.cur.execute("create table if not exists book(id INTEGER PRIMARY KEY, title text,author text,year integer, isbn integer)")
        self.conn.commit()

    def insert(self,title, author,year,isbn):
        self.cur.execute("insert into book values(NULL,?,?,?,?)",(title, author,year,isbn))
        self.conn.commit()

    def view(self):
        self.cur.execute("select * from book")
        rows=self.cur.fetchall()
        return rows

    def search(self,title="", author="",year="",isbn=""):
        self.cur.execute("select * from book where title=? or author=? or year=? or isbn=?",(title, author,year,isbn))
        rows=self.cur.fetchall()
        return rows

    def delete(self,id):
        self.cur.execute("delete from book where id=?",(id,))#dont forget the comma
        self.conn.commit()

    def update(self,id, title,author,year,isbn):
        self.cur.execute("update book set title=?,author=?,year=?,isbn=? where id=?",(title,author,year,isbn,id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

database=Database("books.db")


class Window(object):
    def __init__(self,window):
        self.window=window             #Tk()
        self.selected_tuple=()
        self.window.wm_title("Book Store")

        l1=Label(window,text="Title")
        l1.grid(row=0,column=0)
        l2=Label(window,text="Author")
        l2.grid(row=0,column=2)
        l3=Label(window,text="Year")
        l3.grid(row=1,column=0)
        l4=Label(window,text="ISBN")
        l4.grid(row=1,column=2)

        self.title_text=StringVar()
        self.e1=Entry(window,textvariable=self.title_text)
        self.e1.grid(row=0,column=1)

        self.author_text=StringVar()
        self.e2=Entry(window,textvariable=self.author_text)
        self.e2.grid(row=0,column=3)

        self.year_text=StringVar()
        self.e3=Entry(window,textvariable=self.year_text)
        self.e3.grid(row=1,column=1)

        self.isbn_text=StringVar()
        self.e4=Entry(window,textvariable=self.isbn_text)
        self.e4.grid(row=1,column=3)

        self.list1=Listbox(window,height=10,width=25)
        self.list1.grid(row=2,column=0,rowspan=6,columnspan=2)

        self.sb1=Scrollbar(window)
        self.sb1.grid(row=2,column=2,rowspan=6)
        self.list1.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.list1.yview)

        self.list1.bind('<<ListboxSelect>>',self.get_selected_row)

        b1=Button(window,text="View all",width=12,command=self.view_command)
        b1.grid(row=2,column=3)
        b2=Button(window,text="Search entry",width=12,command=self.search_command)
        b2.grid(row=3,column=3)
        b3=Button(window,text="Add entry",width=12,command=self.add_command)
        b3.grid(row=4,column=3)
        b4=Button(window,text="Update",width=12,command=self.update_command)
        b4.grid(row=5,column=3)
        b5=Button(window,text="Delete",width=12,command=self.delete_command)
        b5.grid(row=6,column=3)
        b6=Button(window,text="Close",width=12,command=self.window.destroy)
        b6.grid(row=7,column=3)


    def get_selected_row(self,event): #function happen when there is a click event

        if self.list1.size!=0:
            self.index=self.list1.curselection()[0]
            self.selected_tuple=self.list1.get(self.index)
            self.e1.delete(0,END)
            self.e1.insert(END,self.selected_tuple[1])
            self.e2.delete(0,END)
            self.e2.insert(END,self.selected_tuple[2])
            self.e3.delete(0,END)
            self.e3.insert(END,self.selected_tuple[3])
            self.e4.delete(0,END)
            self.e4.insert(END,self.selected_tuple[4])

    def view_command(self):
        self.list1.delete(0,END)
        for row in database.view():
            self.list1.insert(END,row)


    def search_command(self):
        self.list1.delete(0,END)
        for row in database.search(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get()):
            self.list1.insert(END,row)

    def add_command(self):
        database.insert(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get())
        self.list1.delete(0,END)
        self.list1.insert(END,(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get()))

    def delete_command(self):
        database.delete(self.selected_tuple[0])

    def update_command(self):
        database.update(self.selected_tuple[0],self.title_text.get(),self.author_text.get(),self.year_text.get(),self.isbn_text.get())




window=Tk()
Window(window)
window=mainloop()
