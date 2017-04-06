# controller.py
from model import Book, Person, OlvBook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#----------------------------------------------------------------------
def addRecord(data):
    """
    Data should be a tuple of two dictionaries in the following format:
    
    ("author":{"first_name":"John", "last_name":"Doe"},
     "book":{"title":"Some book", "isbn":"1234567890", 
             "publisher":"Packt"}
    )
    """
    book = Book()
    book.title = data["book"]["title"]
    book.isbn = data["book"]["isbn"]
    book.publisher = data["book"]["publisher"]
    author = Person()
    author.first_name = data["author"]["first_name"]
    author.last_name = data["author"]["last_name"]
    book.person = author
    
    # connect to session and commit data to database
    session = connectToDatabase()
    session.add(book)
    session.commit()
    session.close()
    
#----------------------------------------------------------------------
def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine("sqlite:///devdata.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

#----------------------------------------------------------------------
def convertResults(results):
    """
    Convert results to OlvBook objects
    """
    print
    books = []
    for record in results:
        author = "%s %s" % (record.person.first_name, 
                            record.person.last_name)
        book = OlvBook(record.id, record.title, author,
                       record.isbn, record.publisher,
                       record.person.last_name,
                       record.person.first_name
                       )
        books.append(book)
    return books

#----------------------------------------------------------------------
def deleteRecord(idNum):
    """
    Delete a record from the database
    """
    session = connectToDatabase()
    record = session.query(Book).filter_by(id=idNum).one()
    session.delete(record)
    session.commit()
    session.close()
    
#----------------------------------------------------------------------
def editRecord(idNum, row):
    """
    Edit a record
    """
    session = connectToDatabase()
    record = session.query(Book).filter_by(id=idNum).one()
    print
    record.title = row["title"]
    record.person.first_name = row["first_name"]
    record.person.last_name = row["last_name"]
    record.isbn = row["isbn"]
    record.publisher = row["publisher"]
    session.add(record)
    session.commit()
    session.close()

#----------------------------------------------------------------------
def getAllRecords():
    """
    Get all records and return them
    """
    session = connectToDatabase()
    result = session.query(Book).all()
    books = convertResults(result)
    session.close()
    return books

#----------------------------------------------------------------------
def searchRecords(filterChoice, keyword):
    """
    Searches the database based on the filter chosen and the keyword
    given by the user
    """
    session = connectToDatabase()
    if filterChoice == "Author":
        qry = session.query(Person)
        result = qry.filter(Person.first_name.contains('%s' % keyword)).all()
        records = []
        for record in result:
            for book in record.books:
                records.append(book)
        result = records
        print result
    elif filterChoice == "Title":
        qry = session.query(Book)
        result = qry.filter(Book.title.contains('%s' % keyword)).all()
    elif filterChoice == "ISBN":
        qry = session.query(Book)
        result = qry.filter(Book.isbn.contains('%s' % keyword)).all()
    else:
        qry = session.query(Book)
        result = qry.filter(Book.publisher.contains('%s' % keyword)).all()    
    books = convertResults(result)
    print
    return books