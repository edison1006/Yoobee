class LibraryItem:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrower = None

    def display_details(self):
        return f"Title: {self.title}, Author: {self.author}"


class Book(LibraryItem):
    def display_details(self):
        return f"[Book] {super().display_details()}"


class Magazine(LibraryItem):
    def __init__(self, title, author, issue_frequency):
        super().__init__(title, author)
        self.issue_frequency = issue_frequency

    def display_details(self):
        return f"[Magazine] {super().display_details()}, Issue Frequency: {self.issue_frequency}"


class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def borrow_item(self, title, borrower):
        for item in self.items:
            if item.title == title and not item.is_borrowed:
                item.is_borrowed, item.borrower = True, borrower
                return f"{title} borrowed by {borrower}."
        return f"{title} not available."

    def return_item(self, title):
        for item in self.items:
            if item.title == title and item.is_borrowed:
                item.is_borrowed, item.borrower = False, None
                return f"{title} returned."
        return f"{title} was not borrowed."

    def display_all(self):
        for item in self.items:
            status = "Available" if not item.is_borrowed else f"Borrowed by {item.borrower}"
            print(f"{item.display_details()} | {status}")


if __name__ == "__main__":
    library = Library()
    library.add_item(Book("War and Peace", "Leo Tolstoy"))
    library.add_item(Book("Anna Karenina", "Leo Tolstoy"))
    library.add_item(Magazine("Time", "Time Editorial Team", "Weekly"))

    print("Library Items:")
    library.display_all()

    print(library.borrow_item("War and Peace", "Tom"))
    print(library.return_item("War and Peace"))

    print("\nUpdated Library Items:")
    library.display_all()
