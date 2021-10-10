import sqlite3
import pytest


@pytest.fixture
def setup_database():
    """ Fixture to set up the in-memory database with test data """
    con = sqlite3.connect(':memory:')
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE users(name text, status text, mail text)''')
    sample_users = [
        ('Per', 'Seller', 'per@test.com'),
        ('Arne', 'Buyer', 'arne1@grp18.no'),
    ]
    cursor.executemany('INSERT INTO users VALUES(?, ?, ?)', sample_users)
    yield con


def test_connection(setup_database):
    # Test to make sure that there are 2 items in the database
    cursor = setup_database
    assert len(list(cursor.execute('SELECT * FROM users'))) == 2


def test_add_to_table(setup_database):
    # Test to add to the table
    cursor = setup_database
    cursor.execute('''INSERT INTO users VALUES('Mona', 'Buyer', 'mona.lisa@gmail.com')''')
    assert len(list(cursor.execute('SELECT * FROM users'))) == 3


def test_remove_from_table(setup_database):
    # Test to remove from table
    cursor = setup_database
    cursor.execute('''DELETE FROM users WHERE name = "Mona" ''')
    assert len(list(cursor.execute('SELECT * FROM users'))) == 2


def test_for_mail_already_in_use(setup_database):
    # Testing if there are more than one of the mail in the table
    cursor = setup_database
    mail = "Epost@test.com"
    cursor.execute('''INSERT INTO users VALUES('Epost', 'Buyer', ?)''', (mail,))
    # cursor.execute('''INSERT INTO users VALUES('Hei', 'Seller', ?)''', (mail,))
    assert len(list(cursor.execute("SELECT * FROM users WHERE mail= ?", (mail,)))) == 1


def test_for_at_sign_in_mail():
    # Testing if char (@) exists
    mail = "Epost@test.com"
    AT_SIGN = "@"
    if AT_SIGN in mail:
        assert True
    else:
        assert False


def test_if_name_exists(setup_database):
    # Testing if name already exists
    # --- Mest for å prøve, kan bygges på videre
    cursor = setup_database
    liste = list(cursor.execute("SELECT name FROM users"))
    name = ('Per',)
    for i in liste:
        assert i == name or 'Arne'

