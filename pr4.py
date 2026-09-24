import json
from collections import namedtuple

from fastapi import FastAPI, Response

app: FastAPI = FastAPI()

book = namedtuple("book", ["id", "title", "author"])
BOOKS = [
    book(1, "1984", "George Orwell"),
    book(2, "To Kill a Mockingbird", "Harper Lee"),
    book(3, "The Great Gatsby", "F. Scott Fitzgerald"),
    book(4, "Pride and Prejudice", "Jane Austen"),
    book(5, "The Catcher in the Rye", "J.D. Salinger"),
    book(6, "Moby-Dick", "Herman Melville"),
    book(7, "War and Peace", "Leo Tolstoy"),
    book(8, "The Odyssey", "Homer"),
    book(9, "Crime and Punishment", "Fyodor Dostoevsky"),
    book(10, "The Hobbit", "J.R.R. Tolkien"),
    book(11, "Fahrenheit 451", "Ray Bradbury"),
    book(12, "Jane Eyre", "Charlotte Bronte"),
    book(13, "Wuthering Heights", "Emily Bronte"),
    book(14, "Brave New World", "Aldous Huxley"),
    book(15, "The Lord of the Rings", "J.R.R. Tolkien"),
    book(16, "Anna Karenina", "Leo Tolstoy"),
    book(17, "The Divine Comedy", "Dante Alighieri"),
    book(18, "Don Quixote", "Miguel de Cervantes"),
    book(19, "Frankenstein", "Mary Shelley"),
    book(20, "Dracula", "Bram Stoker"),
    book(21, "The Picture of Dorian Gray", "Oscar Wilde"),
    book(22, "Les Misérables", "Victor Hugo"),
    book(23, "The Count of Monte Cristo", "Alexandre Dumas"),
    book(24, "One Hundred Years of Solitude", "Gabriel García Márquez"),
    book(25, "The Brothers Karamazov", "Fyodor Dostoevsky"),
]


@app.get("/books")
def get_books():
    books = [
        {"id": id, "title": title, "author": author} for (id, title, author) in BOOKS
    ]
    return Response(
        status_code=200, content=json.dumps(books), media_type="application/json"
    )


@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    if book_id <= 0 or book_id > len(BOOKS):
        return Response(
            status_code=422,
            content=json.dumps({"error": "book_id is incorrect", "book_id": book_id}),
            media_type="application/json",
        )

    for id, title, author in BOOKS:
        if id == book_id:
            temp_book = {"id": id, "title": title, "author": author}
            return Response(
                status_code=200,
                content=json.dumps(temp_book),
                media_type="application/json",
            )

    return Response(
        status_code=404,
        content=json.dumps({"error": "Book not found"}),
        media_type="application/json",
    )


@app.get("/books/by-author/{temp_author}")
def get_books_by_author(temp_author: str):
    books = []
    for id, title, author in BOOKS:
        if author == temp_author:
            books.append({"id": id, "title": title, "author": author})
            return Response(
                status_code=200,
                content=json.dumps(books),
                media_type="application/json",
            )

    return Response(
        status_code=404,
        content=json.dumps({"error": "Books not found"}),
        media_type="application/json",
    )


@app.get("/authors")
def get_authors():
    authors = [book.author for book in BOOKS]
    return Response(
        status_code=200, content=json.dumps(authors), media_type="application/json"
    )
