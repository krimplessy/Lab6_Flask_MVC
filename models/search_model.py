import pandas as pd
import numpy as np


def get_genre(conn):
    return pd.read_sql("""
 SELECT genre_name,count(b.book_id) as counting
 FROM genre 
 join book b on genre.genre_id = b.genre_id 
 group by genre_name
 order by genre_name
 """, conn)


def get_author(conn):
    return pd.read_sql("""
 SELECT a.author_name,count(ba.book_id) as counting
 FROM book_author ba
 join author a on ba.author_id = a.author_id
 group by ba.author_id
 order by a.author_name
 """, conn)


def get_publisher(conn):
    return pd.read_sql("""
 SELECT publisher_name, count(b.book_id) 
 FROM publisher 
 join book b on publisher.publisher_id = b.publisher_id
 group by publisher_name
 order by publisher_name
 """, conn)


def get_book_info(conn, g, a, p):
    genre_list = g
    author_list = a
    publisher_list = p
    df = pd.read_sql("""select * from book_info;""", conn)
    if genre_list:
        df = df[df.Жанр.isin(genre_list)]
    if author_list:
        df1 = pd.read_sql(f'''select author_name, ba.book_id from author
                join book_author ba on author.author_id = ba.author_id;''', conn)
        df1 = df1[df1.author_name.isin(author_list)]
        df = df[df.book_id.isin(df1.book_id)]

    if publisher_list:
        df = df[df.Издательство.isin(publisher_list)]

    df = df.reset_index(drop=True)
    return df


# для обработки данных о взятой книге
def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    available = pd.read_sql(f'''
       select available_numbers from book
       WHERE book_id = {book_id};''', conn)
    if available.values[0][0] != 0:
        cur.executescript(f'''
        UPDATE book
        SET available_numbers = available_numbers - 1
        WHERE book_id = {book_id} and available_numbers>0;
        INSERT INTO book_reader (book_id, reader_id, borrow_date, return_date)
        VALUES ({book_id}, {reader_id}, DATE(), null);
        ''')
    # добавить взятую книгу (book_id) читателю (reader_id) в таблицу book_reader
    # указать текущую дату как дату выдачи книги
    # уменьшить количество экземпляров взятой книги
    conn.commit()


def create_info(conn):
    cur = conn.cursor()
    cur.executescript("""
    drop view if exists book_info;
    """)
    cur.executescript("""
    create view book_info as
                     SELECT b.book_id as book_id, b.title as Название, 
                     group_concat(a.author_name, ', ')  as Авторы,
                     g.genre_name as Жанр,   p.publisher_name as Издательство,
                     b.year_publication as ГодИздательства, b.available_numbers as Количество
                     FROM book_author
                     join book b on book_author.book_id = b.book_id
                     join author a on book_author.author_id = a.author_id
                     join genre g on b.genre_id = g.genre_id
                     join publisher p on b.publisher_id = p.publisher_id
                     group by b.title order by b.title;
                     """)
    conn.commit()