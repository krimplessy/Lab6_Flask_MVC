import models.search_model as model
from app import app
from flask import render_template, request, session,redirect
from utils import get_db_connection


@app.route('/search', methods=['get'])
def search():
    conn = get_db_connection()
    if request.values.get('book'):
        book_id = request.values.get('book')
        model.borrow_book(conn, book_id, session['reader_id'])
        print(str(session['reader_id']))
        return redirect('/?reader=' + str(session['reader_id']))
        flash(hi)

    if request.values.get('genre'):
        genre_list = request.values.getlist('genre')
    else:
        genre_list = []
    if request.values.get('author'):
        author_list = request.values.getlist('author')
    else:
        author_list = []
    if request.values.get('publisher'):
        publisher_list = request.values.getlist('publisher')
    else:
        publisher_list = []


    model.create_info(conn)
    df_book_info = model.get_book_info(conn, genre_list, author_list, publisher_list)
    df_genre = model.get_genre(conn)
    df_author = model.get_author(conn)
    df_publisher = model.get_publisher(conn)
    conn.close()

    # генерируем результат на основе шаблона
    html = render_template(
        'search.html',
        genre=df_genre,
        author=df_author,
        publisher=df_publisher,
        book_info=df_book_info,
        len=len,
        print=print,

        genre_list=genre_list,
        author_list=author_list,
        publisher_list=publisher_list
    )
    return html