import mysql.connector
from faker import Faker
import random

fake = Faker()

# Define genres
genres = ["Fiction", "Non-fiction", "Mystery", "Fantasy",
          "Romance", "Sci-fi", "Horror", "Biography", "History"]

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
for _ in range(100):
    name = fake.name().split()
    first_name = name[0]
    last_name = name[1]
    add_author = ("INSERT INTO Author (firstName, lastName) VALUES (%s, %s)")
    data_author = (first_name, last_name)
    cursor.execute(add_author, data_author)

# Generate publishers
# for _ in range(100):
#     title = fake.company()
#     add_publisher = ("INSERT INTO Publisher (title) VALUES (%s)")
#     data_publisher = (title,)
#     cursor.execute(add_publisher, data_publisher)

# Generate books
# for _ in range(100):
#     title = fake.catch_phrase()
#     publishYear = random.randint(1950, 2023)
#     idAuthor = random.randint(1, 100)
#     idPublisher = random.randint(1, 100)
#     add_book = ("INSERT INTO Book (title, publishYear, idAuthor, idPublisher) VALUES (%s, %s, %s, %s)")
#     data_book = (title, publishYear, idAuthor, idPublisher)
#     cursor.execute(add_book, data_book)

# Generate genres
# for genre in genres:
#     add_genre = ("INSERT INTO Genre (title) VALUES (%s)")
#     data_genre = (genre,)
#     cursor.execute(add_genre, data_genre)

# Generate book stores
# for _ in range(100):
#     city = fake.city()
#     street = fake.street_name()
#     add_book_store = ("INSERT INTO BookStore (city, street) VALUES (%s, %s)")
#     data_book_store = (city, street)
#     cursor.execute(add_book_store, data_book_store)

# Generate librarians
# for _ in range(100):
#     name = fake.name().split()
#     first_name = name[0]
#     last_name = name[1]
#     idBookStore = random.randint(1, 100)
#     add_librarian = ("INSERT INTO Librarian (firstName, lastName, idBookStore) VALUES (%s, %s, %s)")
#     data_librarian = (first_name, last_name, idBookStore)
#     cursor.execute(add_librarian, data_librarian)

# Generate customers and memberships
# for _ in range(100):
#     name = fake.name().split()
#     first_name = name[0]
#     last_name = name[1]
#     birthYear = random.randint(1950, 2005)
#     add_customer = ("INSERT INTO Customer (firstName, lastName, birthYear) VALUES (%s, %s, %s)")
#     data_customer = (first_name, last_name, birthYear)
#     cursor.execute(add_customer, data_customer)
#     customer_id = cursor.lastrowid
#     expiredDate = fake.date_between(start_date='-3y', end_date='+1y')
#     lastActiveMembershipTypeId = random.randint(1, 5)
#     add_membership = ("INSERT INTO ActiveMembership (expiredDate, lastActiveMembershipTypeId) VALUES (%s, %s)")
#     data_membership = (expiredDate, lastActiveMembershipTypeId)
#     cursor.execute(add_membership, data_membership)
#     membership_id = cursor.lastrowid
#     update_customer = ("UPDATE Customer SET membershipId = %s WHERE idCustomer = %s")
#     data_update_customer = (membership_id, customer_id)
#     cursor.execute(update_customer, data_update_customer)

cnx.commit()
cursor.close()
cnx.close()
