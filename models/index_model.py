import pandas

#Список читателей
def get_reader(conn):
    return pandas.read_sql(
        '''
        SELECT * FROM reader
        ''', conn)


# выбираем и выводим записи о том, какие книги брал читатель
def get_book_reader(conn, reader_id):
    return pandas.read_sql('''
     WITH get_authors( book_id, authors_name)
     AS(
     SELECT book_id, GROUP_CONCAT(author_name)
     FROM author JOIN book_author USING(author_id)
     GROUP BY book_id
     )
     SELECT title AS Название, authors_name AS Авторы,
     borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
     book_reader_id
     FROM
     reader
     JOIN book_reader USING(reader_id)
     JOIN book USING(book_id)
     JOIN get_authors USING(book_id)
     WHERE reader.reader_id = :id
     ORDER BY 3
     ''', conn, params={"id": reader_id})
    return cur.lastrowid


# Взять книгу
def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    # добавить взятую книгу (book_id) читателю (reader_id) в таблицу book_reader
    # указать текущую дату как дату выдачи книги
    # уменьшить количество экземпляров взятой книги
    return pandas.read_sql('''
    UPDATE book
        SET available_numbers = available_numbers - 1
        WHERE book_id = b_id and available_numbers>0;
    
        INSERT INTO book_reader (book_id, reader_id, borrow_date, return_date)
        VALUES (b_id, r_id, DATE(), null);
    
    ''',conn,params={"r_id": reader_id, "b_id":book_id})
    return True


#Сдать книгу
def return_book(conn, reader_book_id):
    cur = conn.cursor()
    cur.executescript(f'''
    UPDATE book
    SET available_numbers = available_numbers + 1
    WHERE book_id = (SELECT book_id FROM book_reader WHERE return_date IS NULL and book_reader_id = {reader_book_id});

    UPDATE book_reader
    SET return_date = DATE()
    WHERE book_reader_id = {reader_book_id}
        ''')
    return conn.commit()

#Добавить нового читателя
def get_new_reader(conn, newReaderFio):
    cur = conn.cursor()
    cur.executescript(
    f'''
        INSERT INTO reader (reader_name)
        VALUES ('{newReaderFio}');
    ''')
    conn.commit()
    return pandas.read_sql('''SELECT MAX(reader_id) FROM reader LIMIT 1;''', conn).values[0][0];

