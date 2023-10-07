import sqlite3

def create_table():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (title text, author text, publisher text, description text, category text)''')

    conn.commit()
    conn.close()
    
def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    publisher = input("Enter book publisher: ")
    description = input("Enter book description: ")
    category = input("Enter book category: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?)", (title, author, publisher, description, category))

    conn.commit()
    conn.close()

    print("Book added successfully.")

def search_book():
    keyword = input("Enter search keyword: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ? OR description LIKE ? OR category LIKE ?", ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))

    results = c.fetchall()

    conn.close()

    if len(results) == 0:
        print("No books found.")
    else:
        for book in results:
            print(f"Name: {book[0]}, Author: {book[1]}, Publisher: {book[2]}, Description: {book[3]}, Category: {book[4]}")

def delete_book():
    title_to_delete = input("Enter the title of the book to delete: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM books WHERE title=?", (title_to_delete,))
    book_to_delete = c.fetchone()

    if book_to_delete:
        confirmation = input(f"Are you sure you want to delete this book: {', '.join(book_to_delete[:-1])}? (yes/no): ")
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
        print(f"Current book information: {', '.join(book_to_modify[:-1])}")
        new_title = input("Enter new title (leave blank to keep current): ")
        new_author = input("Enter new author (leave blank to keep current): ")
        new_publisher = input("Enter new publisher (leave blank to keep current): ")
        new_description = input("Enter new description (leave blank to keep current): ")
        new_category = input("Enter new category (leave blank to keep current): ")

        if new_title:
            book_to_modify = (new_title, new_author, new_publisher, new_description, new_category, title_to_modify)
            c.execute("UPDATE books SET title=?, author=?, publisher=?, description=?, category=? WHERE title=?", book_to_modify)
            conn.commit()
            print("Book information updated successfully.")
        else:
            print("No changes made.")
    else:
        print("Book not found.")

    conn.close()
def display_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM books")

    results = c.fetchall()

    conn.close()

    if len(results) == 0:
        print("No books found.")
    else:
        for book in results:
            print(f"Name: {book[0]}, Author: {book[1]}, Publisher: {book[2]}, Description: {book[3]}, Category: {book[4]}")
def main():
    create_table()

    while True:
        print("1. Add book")
        print("2. Search book")
        print("3. Delete book")
        print("4. Modify book")
        print("5. Display all books")
        print("6. Exit")

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
            display_all_books()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()