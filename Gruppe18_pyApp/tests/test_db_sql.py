import sqlite3
import pytest


@pytest.fixture
def setup_database():
    """ Fixture to set up the in-memory database with test data """
    con = sqlite3.connect(':memory:')
    cursor = con.cursor()
    cursor.execute('''
	    CREATE TABLE users
        (name text, type text)''')
    sample_users = [
        ('Per', 'Seller'),
        ('Arne', 'Buyer'),
    ]
    cursor.executemany('INSERT INTO users VALUES(?, ?)', sample_users)
    yield con


def test_connection(setup_database):
    # Test to make sure that there are 2 items in the database
    cursor = setup_database
    assert len(list(cursor.execute('SELECT * FROM users'))) == 2


def test_add_to_db(setup_database):
    # Test to add to the db
    cursor = setup_database
    cursor.execute('''INSERT INTO users VALUES('Mona', 'Buyer')''')
    assert len(list(cursor.execute('SELECT * FROM users'))) == 3


