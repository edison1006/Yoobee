# Base class
class LibraryItem:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrower = None

    def display_details(self):
        return f"Title: {self.title}, Author: {self.author}"


# Book inherits from LibraryItem
class Book(LibraryItem):
    def __init__(self, title, author):
        super().__init__(title, author)

    def display_details(self):
        return f"[Book] Title: {self.title}, Author: {self.author}"


# Magazine inherits from LibraryItem
class Magazine(LibraryItem):
    def __init__(self, title, author, issue_frequency):
        super().__init__(title, author)
        self.issue_frequency = issue_frequency

    def display_details(self):
        return (f"[Magazine] Title: {self.title}, Author: {self.author}, "
                f"Issue Frequency: {self.issue_frequency}")


# Library manages all items
class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item: LibraryItem):
        self.items.append(item)

    def remove_item(self, title):
        self.items = [item for item in self.items if item.title != title]

    def borrow_item(self, title, borrower_name):
        for item in self.items:
            if item.title == title and not item.is_borrowed:
                item.is_borrowed = True
                item.borrower = borrower_name
                return f"{title} has been borrowed by {borrower_name}."
        return f"{title} is not available."

    def return_item(self, title):
        for item in self.items:
            if item.title == title and item.is_borrowed:
                item.is_borrowed = False
                item.borrower = None
                return f"{title} has been returned."
        return f"{title} was not borrowed."

    def display_all_items(self):
        for item in self.items:
            status = "Available" if not item.is_borrowed else f"Borrowed by {item.borrower}"
            print(f"{item.display_details()} | Status: {status}")


if __name__ == "__main__":
    library = Library()

    # Add books and magazines
    book1 = Book("War and Peace", "Leo Tolstoy")
    book2 = Book("Anna Karenina", "Leo Tolstoy")
    mag1 = Magazine("Time", "Time Editorial Team", "Weekly")

    library.add_item(book1)
    library.add_item(book2)
    library.add_item(mag1)

    # Display all items
    print("Library Items:")
    library.display_all_items()

    # Borrow and return
    print(library.borrow_item("War and Peace", "Leo Tolstoy"))
    print(library.return_item("War and Peace"))

    # After borrowing
    print("\n Updated Library Items:")
    library.display_all_items()
