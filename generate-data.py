import mysql.connector
from faker import Faker
import random

AUTHORS_COUNT = 100
PUBLISHERS_COUNT = 100
BOOKS_COUNT = 100
MAX_GENRES_PER_BOOK = 3

BOOK_STORES_COUNT = 100
# at least one librarian per library + extra librarians (LIBRARIANST_COUNT - BOOK_STORES_COUNT)
LIBRARIANS_COUNT = BOOK_STORES_COUNT*4

CUSTOMER_COUNT = 3000

MAX_RENTED_BOOKS_PER_CUSTOMER = 5

fake = Faker()

# Define genres
genres = ["Fiction", "Non-fiction", "Mystery", "Fantasy",
          "Romance", "Sci-fi", "Horror", "Biography", "History"]

membership_types = ["Basic", "Standard", "Premium"]
membership_types_prices = [1000, 2000, 3000]

# MySQL connection
cnx = mysql.connector.connect(
    user='root',
    password='root',
    host='127.0.0.1',
    database='library',
    ssl_disabled=True
)
cursor = cnx.cursor()

# empty tables
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("TRUNCATE TABLE ActiveMembership")
cursor.execute("TRUNCATE TABLE Author")
cursor.execute("TRUNCATE TABLE Book")
cursor.execute("TRUNCATE TABLE BookStore")
cursor.execute("TRUNCATE TABLE Book_has_BookStore")
cursor.execute("TRUNCATE TABLE Book_has_Genre")
cursor.execute("TRUNCATE TABLE Customer")
cursor.execute("TRUNCATE TABLE Genre")
cursor.execute("TRUNCATE TABLE Librarian")
cursor.execute("TRUNCATE TABLE MembershipType")
cursor.execute("TRUNCATE TABLE Publisher")
cursor.execute("TRUNCATE TABLE RentedBook")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


# Generate authors
print("Generating authors...")
for _ in range(AUTHORS_COUNT):
    name = fake.name().split()
    first_name = name[0]
    last_name = name[1]
    add_author = ("INSERT INTO Author (firstName, lastName) VALUES (%s, %s)")
    data_author = (first_name, last_name)
    cursor.execute(add_author, data_author)
print("Authors generated.")
print()

# Generate publishers
print("Generating publishers...")
for _ in range(PUBLISHERS_COUNT):
    title = fake.company()
    add_publisher = ("INSERT INTO Publisher (title) VALUES (%s)")
    data_publisher = (title,)
    cursor.execute(add_publisher, data_publisher)
print("Publishers generated.")
print()

# Generate books
print("Generating books...")
for _ in range(BOOKS_COUNT):
    title = fake.catch_phrase()[0:40]
    publishYear = random.randint(1950, 2023)
    idAuthor = random.randint(1, AUTHORS_COUNT)
    idPublisher = random.randint(1, PUBLISHERS_COUNT)
    add_book = (
        "INSERT INTO Book (title, publishYear, idAuthor, idPublisher) VALUES (%s, %s, %s, %s)")
    data_book = (title, publishYear, idAuthor, idPublisher)
    cursor.execute(add_book, data_book)
print("Books generated.")
print()

# Generate genres
for genre in genres:
    add_genre = ("INSERT INTO Genre (title) VALUES (%s)")
    data_genre = (genre,)
    cursor.execute(add_genre, data_genre)


# books and genres must be present before connecting them
cnx.commit()


# Connect books with genres
for idBook in range(1, BOOKS_COUNT + 1):
    genre_count = random.randint(1, MAX_GENRES_PER_BOOK)

    genres_ids = []
    # make sure "FICTION" and "NON-FICTION" are not present at the same time
    fiction_present = True
    non_fiction_present = True
    while fiction_present and non_fiction_present:
        genres_ids = random.sample(range(1, len(genres) + 1), genre_count)

        fiction_present = False
        non_fiction_present = False
        for idGenre in genres_ids:
            if genres[idGenre - 1] == "Fiction":
                fiction_present = True
            if genres[idGenre - 1] == "Non-fiction":
                non_fiction_present = True

    for idGenre in genres_ids:
        add_book_has_genre = (
            "INSERT INTO Book_has_Genre (idBook, idGenre) VALUES (%s, %s)")
        data_book_has_genre = (idBook, idGenre)
        cursor.execute(add_book_has_genre, data_book_has_genre)

# Generate book stores
print("Generating book stores...")
for _ in range(BOOK_STORES_COUNT):
    city = fake.city()
    address = fake.street_name()
    # add number to street to form an address
    address += " " + str(random.randint(1, 100))
    add_book_store = ("INSERT INTO BookStore (city, address) VALUES (%s, %s)")
    data_book_store = (city, address)
    cursor.execute(add_book_store, data_book_store)
print("Book stores generated.")
print()

cnx.commit()

# Generate librarians
print("Generating librarians...")

# make sure every library has at least one librarian
for idBookStore in range(1, BOOK_STORES_COUNT + 1):
    name = fake.name().split()
    first_name = name[0]
    last_name = name[1]
    add_librarian = (
        "INSERT INTO Librarian (firstName, lastName, idBookStore) VALUES (%s, %s, %s)")
    data_librarian = (first_name, last_name, idBookStore)
    cursor.execute(add_librarian, data_librarian)

for _ in range(LIBRARIANS_COUNT-BOOK_STORES_COUNT):
    name = fake.name().split()
    first_name = name[0]
    last_name = name[1]
    idBookStore = random.randint(1, 100)
    add_librarian = (
        "INSERT INTO Librarian (firstName, lastName, idBookStore) VALUES (%s, %s, %s)")
    data_librarian = (first_name, last_name, idBookStore)
    cursor.execute(add_librarian, data_librarian)
print("Librarians generated.")
print()

# connect books and book stores
print("Connecting books and book stores...")
for idBookStore in range(1, BOOK_STORES_COUNT + 1):
    books_count = random.randint(BOOKS_COUNT * 2 // 10, BOOKS_COUNT)
    books_ids = random.sample(range(1, BOOKS_COUNT + 1), books_count)
    rentedCount = random.randint(1, 20)
    availableCount = random.randint(1, 20)
    for idBook in books_ids:
        add_book_has_book_store = (
            "INSERT INTO Book_has_BookStore (idBook, idBookStore, rentedCount, availableCount) VALUES (%s, %s, %s, %s)")
        data_book_has_book_store = (
            idBook, idBookStore, rentedCount, availableCount)
        cursor.execute(add_book_has_book_store, data_book_has_book_store)
print("Done.")
print()

# Generate customers and memberships

# membership types
for i in range(1, len(membership_types) + 1):
    add_membership_type = (
        "INSERT INTO MembershipType (title, price) VALUES (%s, %s)")
    data_membership_type = (
        membership_types[i - 1], membership_types_prices[i - 1])
    cursor.execute(add_membership_type, data_membership_type)

# active memberships and customers
print("Generating customers and memberships...")
for _ in range(CUSTOMER_COUNT):
    startDate = fake.date_between(start_date='-3y', end_date='+1y')
    expirationDate = fake.date_between(start_date=startDate, end_date='+1y')

    lastActiveMembershipTypeId = random.randint(1, len(membership_types))

    add_active_membership = (
        "INSERT INTO ActiveMembership (startDate, expirationDate, lastActiveMembershipTypeId) VALUES (%s, %s, %s)")

    data_active_membership = (startDate, expirationDate, lastActiveMembershipTypeId)
    cursor.execute(add_active_membership, data_active_membership)

    first_name = fake.first_name()
    last_name = fake.last_name()
    birthYear = random.randint(1950, 2010)
    add_customer = (
        "INSERT INTO Customer (firstName, lastName, birthYear, membershipId) VALUES (%s, %s, %s, %s)")
    data_customer = (first_name, last_name, birthYear, cursor.lastrowid)

    cursor.execute(add_customer, data_customer)
print("Done.")
print()

cnx.commit()

# RentedBook table, connect customers with books
# idCustomer, startRentDate, returnDate, rentLimitDate, idBook, idBookStore
print("Generating rented books...")
for idCustomer in range(1, CUSTOMER_COUNT + 1):
    rented_books_count = random.randint(0, MAX_RENTED_BOOKS_PER_CUSTOMER)

    for _ in range(rented_books_count):
        # get random row from Book_has_BookStore table
        # get idBook, idBookStore
        cursor.execute(
            "SELECT * FROM Book_has_BookStore ORDER BY RAND() LIMIT 1")
        book_has_BookStore_entry = cursor.fetchone()
        # print(book_has_BookStore_entry)

        idBook = book_has_BookStore_entry[0]
        idBookStore = book_has_BookStore_entry[1]

        # connect customer with book

        startRentDate = fake.date_between(start_date='-3y', end_date='today')
        # date when the book is returned
        returnDate = fake.date_between(
            start_date=startRentDate, end_date='+1y')
        # date when the book should be returned
        rentLimitDate = fake.date_between(
            start_date=returnDate, end_date='+1y')

        add_rented_book = (
            "INSERT INTO RentedBook (idCustomer, startRentDate, returnDate, rentLimitDate, idBook, idBookStore) VALUES (%s, %s, %s, %s, %s, %s)")

        data_rented_book = (idCustomer, startRentDate,
                            returnDate, rentLimitDate, idBook, idBookStore)
        cursor.execute(add_rented_book, data_rented_book)
print("Done.")
print()

cnx.commit()
cursor.close()
cnx.close()
