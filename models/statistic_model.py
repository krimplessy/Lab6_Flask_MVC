import pandas
import sqlite3
import pandas as pd

#За вбраннй период ищем самую востребованную книгу
def most_popular_book(conn, dateStart, dateEnd):
    return pd.read_sql(f'''
        SELECT title AS 'Название', count(book_reader_id) as 'Сколько раз брали'
        FROM book
        JOIN book_reader ON (book.book_id = book_reader.book_id)
        WHERE book_reader.borrow_date>='{dateStart}' and book_reader.borrow_date<='{dateEnd}'
        GROUP BY book_reader.book_id
        HAVING count(book_reader_id)=(
            SELECT count(book_reader_id)
            FROM book
            JOIN book_reader ON (book.book_id = book_reader.book_id)
            WHERE book_reader.borrow_date>='{dateStart}' and book_reader.borrow_date<='{dateEnd}'
            GROUP BY book_reader.book_id
            ORDER BY count(book_reader_id) desc limit 1
             )
    ''', conn)

