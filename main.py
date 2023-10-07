import sqlite3

def create_table():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (title text, author text, publisher text, isbn text)''')

    conn.commit()
    conn.close()

def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    publisher = input("Enter book publisher: ")
    isbn = input("Enter book ISBN: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (title, author, publisher, isbn))

    conn.commit()
    conn.close()

    print("Book added successfully.")

def search_book():
    keyword = input("Enter search keyword: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ? OR isbn LIKE ?", ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))

    results = c.fetchall()

    conn.close()

    if len(results) == 0:
        print("No books found.")
    else:
        for book in results:
            print(book)

def delete_book():
    title_to_delete = input("Enter the title of the book to delete: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE title=?", (title_to_delete,))
    book_to_delete = c.fetchone()

    if book_to_delete:
        confirmation = input(f"Are you sure you want to delete this book: {book_to_delete}? (yes/no): ")
        if confirmation.lower() == 'yes':
            c.execute("DELETE FROM books WHERE title=?", (title_to_delete,))
            conn.commit()
            print("Book deleted successfully.")
        else:
            print("Deletion canceled.")
    else:
        print("Book not found.")

    conn.close()

def modify_book():
    title_to_modify = input("Enter the title of the book to modify: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE title=?", (title_to_modify,))
    book_to_modify = c.fetchone()

    if book_to_modify:
        print(f"Current book information: {book_to_modify}")
        new_title = input("Enter new title (leave blank to keep current): ")
        new_author = input("Enter new author (leave blank to keep current): ")
        new_publisher = input("Enter new publisher (leave blank to keep current): ")
        new_isbn = input("Enter new ISBN (leave blank to keep current): ")

        if new_title:
            book_to_modify = (new_title, new_author, new_publisher, new_isbn)
            c.execute("UPDATE books SET title=?, author=?, publisher=?, isbn=? WHERE title=?", (*book_to_modify, title_to_modify))
            conn.commit()
            print("Book information updated successfully.")
        else:
            print("No changes made.")
    else:
        print("Book not found.")

    conn.close()

def main():
    create_table()

    while True:
        print("1. Add book")
        print("2. Search book")
        print("3. Delete book")
        print("4. Modify book")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            search_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            modify_book()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
