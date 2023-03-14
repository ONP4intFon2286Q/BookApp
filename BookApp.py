class User:
    def __init__(self, name, email):
        self.name, self.email, self.books = name, email, {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print(f"New email: {self.email}")

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        ratings = [rating for rating in self.books.values() if isinstance(rating, int)]
        return sum(ratings) / len(ratings) if ratings else 0

    def __repr__(self):
        return f"User: {self.name}, email: {self.email}"

    def __eq__(self, other_user):
        return isinstance(other_user, self.__class__) and self.name == other_user.name and self.email == other_user.email


class Book:
    def __init__(self, title, isbn):
        self.title, self.isbn, self.ratings = title, isbn, []

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print(f"{self.title} ISBN has been updated to {self.isbn}")

    def add_rating(self, rating):
        print(rating)
        if rating in range(5):
            self.ratings.append(rating)
        else:
            print("\n Invalid Rating \n")

    def get_average_rating(self):
        return int(sum(self.ratings) / len(self.ratings)) if self.ratings else "No ratings"

    def __eq__(self, other_book):
        return isinstance(other_book, self.__class__) and self.title == other_book.title and self.isbn == other_book.isbn

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return self.title


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def __repr__(self):
        return f'"{self.title}" by {self.author}'


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject, self.level = subject, level

    def __repr__(self):
        return f'"{self.title}", a {self.level} manual on {self.subject}'


class BookApp:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbnDic = {}

    def create_book(self, title, isbn):
        self.isbnDic[title] = isbn
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        self.isbnDic[title] = isbn
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        self.isbnDic[title] = isbn
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email)
        if user is None:
            print(f"No user with email {email}")
            return

        user.read_book(book, rating)
        book.add_rating(rating)

        self.books[book] = self.books.get(book, 0) + 1

    def add_user(self, name, email, user_books=None):
        if not email.endswith(('.com', '.edu', '.org')) or '@' not in email:
            print(f"Invalid email for {name} {email}")
            return

        if email in self.users:
            print(f"User {email} already exists.")
            return

        user = User(name, email)
        self.users[email] = user

        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def print_isbnDic(self):
        for title, isbn in self.isbnDic.items():
            print(title, isbn)

    def get_most_read_book(self):
        most_read_book = max(self.books, key=self.books.get, default=None)
        if most_read_book:
            return most_read_book.title, self.books[most_read_book]
        else:
            return None, 0

    def highest_rated_book(self):
        highest_rated_book = max((book for book in self.books.keys() if book.get_average_rating() != 'No ratings'), key=lambda book: book.get_average_rating(), default=None)
        if highest_rated_book:
            return highest_rated_book.title, highest_rated_book.get_average_rating()
        else:
            return None, 'No ratings'

    def most_positive_user(self):
        most_positive_user = max((user for user in self.users.values() if user.get_average_rating() != 'No ratings'), key=lambda user: user.get_average_rating(), default=None)
        if most_positive_user:
            return most_positive_user.name, most_positive_user.get_average_rating()
        else:
            return None, 'No ratings'

    def __repr__(self):
        return f"There are {len(self.users)} users and {len(self.books)} books in BookApp!"

Book_App = BookApp()

# Create a few books:
book1 = Book_App.create_book("Society of Mind", 12345678)
novel1 = Book_App.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
nonfiction1 = Book_App.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Book_App.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Book_App.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Book_App.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)


# Create users:
Book_App.add_user("Alan Turing", "alan@turing.com")
Book_App.add_user("David Marr", "david@computation.org")
# Add a user with three books already read:
Book_App.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])



# Add books with ratings:
Book_App.add_book_to_user(book1, "alan@turing.com", 1)
Book_App.add_book_to_user(novel1, "alan@turing.com", 3)
Book_App.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Book_App.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Book_App.add_book_to_user(novel3, "alan@turing.com", 1)
Book_App.add_book_to_user(novel2, "marvin@mit.edu", 2)
Book_App.add_book_to_user(novel3, "marvin@mit.edu", 2)
Book_App.add_book_to_user(novel3, "david@computation.org", 4)
Book_App.add_book_to_user(novel3, "bin@computation.org", 20)

# Test the functions:
print("\nCatalog: \n")
Book_App.print_catalog()

print("\nUsers: \n")
Book_App.print_users()

print("\nISBN: \n")
Book_App.print_isbnDic()
