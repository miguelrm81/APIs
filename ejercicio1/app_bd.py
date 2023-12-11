# import json
from flask import Flask, request, jsonify
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

# 0.Ruta para obtener todos los libros
@app.route('/books', methods=['GET'])

def all_books():
    conexion = sqlite3.connect('books.db')
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conexion.close()
    return jsonify({'books': books})


# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/books/autor', methods=['GET'])

def book_autor():
    conexion = sqlite3.connect('books.db')
    cursor = conexion.cursor()
    query = """
        SELECT author, COUNT(*) as book_count
        FROM books
        GROUP BY author
        ORDER BY book_count DESC
        """
    cursor.execute(query)
    book = cursor.fetchall()
    conexion.close()
    return jsonify({'libros_autor': book})

# 2.Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/books/autor/<author>', methods=['GET'])
def books_autorV2(author):
    
    conexion = sqlite3.connect('books.db')
    cursor = conexion.cursor()
    query = "SELECT * FROM books WHERE author = ?"
    cursor.execute(query, (author,))
    books_by_author = cursor.fetchall()
    conexion.close()
    return jsonify({'books_autor': books_by_author})

# 3.Ruta para obtener los libros filtrados por título, publicación y autor

@app.route('/books/filtro', methods=['GET'])
def books_filtro():
    conexion = sqlite3.connect('books.db')
    cursor = conexion.cursor()
    title = request.args.get('title', '')
    publi = request.args.get('published', '')
    autor = request.args.get('author', '')
    query = """
        SELECT *
        FROM books
        WHERE title LIKE ? AND published LIKE ? AND author LIKE ?
        """
    cursor.execute(query, ('%' + title + '%', '%' + publi + '%', '%' + autor + '%'))
    books = cursor.fetchall()
    conexion.close()
    return jsonify({'libro_filtro': books})


app.run()