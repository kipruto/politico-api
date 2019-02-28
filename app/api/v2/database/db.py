import os
import psycopg2
from flask import current_app
from app.api.v2.database.tables import create_queries, destroy_queries


class Connection:

    def __init__(self):
        if current_app.config['TESTING']:
            URL = os.getenv('TEST_DATABASE_URL')
        else:
            URL = os.getenv('DATABASE_URL')
        self.connection = psycopg2.connect(URL)
        self.cursor = self.connection.cursor()

    def connection(self):
        """This function creates a connection to the database"""
        return self.connection

    def create_tables(self):
        """This function creates tables in the database"""
        queries = create_queries()
        for query in queries:
            self.cursor.execute(query)
        self.connection.commit()

    def drop_tables(self):
        """This function destroys tables in the database"""
        statements = destroy_queries()
        for statement in statements:
            self.cursor.execute(statement)
        self.connection.commit()

    def drop(self, table):
        self.cursor.execute(
            "DROP TABLE IF IT EXISTS {} CASCADE;".format(table))
        value = self.connection.commit()
        return value

    def insert(self, table, data):
        """ insert data """
        keys = ', '.join([key for key in data])
        values = str(tuple([data[key] for key in data]))
        self.cursor.execute(
            """ INSERT INTO {}({}) VALUES {} """.format(table, keys, values))
        value = self.connection.commit()
        return value

    def fetch_all_items(self, table):
        """ Fetch all items """
        self.cursor.execute("""SELECT * FROM {}""".format(table))
        items = self.cursor.fetchall()
        return items

    def fetch_single_item(self, table, id):
        """ Fetch single item """
        self.cursor.execute(
            """SELECT * FROM {} WHERE {} = {}""".format(table, id, id))
        item = self.cursor.fetchall()
        return item

    def fetch_item_multiple_conditions(self, table, parameter1, parameter2):
        """ Get specific item """
        self.cursor.execute(
            """SELECT * FROM {} WHERE {} = {} and {} = {}""".format(table, parameter1, parameter1, parameter2, parameter2))
        item = self.cursor.fetchall()
        return item

    def search_by_name(self, table, name):
        """ Search specific item """
        self.cursor.execute(
            """SELECT * FROM {} WHERE name='%s'""".format(table) % (name))
        item = self.cursor.fetchall()
        return item

    def search_by_email(self, table, email):
        """ Search specific item """
        self.cursor.execute(
            """SELECT * FROM {} WHERE email='%s'""".format(table) % (email))
        item = self.cursor.fetchone()
        return item

    def delete(self, table, id):
        """ Delete a specific item from table """
        self.cursor.execute(
            """DELETE FROM {} WHERE id = {}""".format(table, id))
        return self.connection.commit()

    def fetch_candidate(self, selector, value):
        self.cursor.execute(""" SELECT users.firstname, users.lastname, offices.name, parties.name
                        FROM candidates INNER JOIN users ON candidates.candidate=users.id
                        INNER JOIN offices ON candidates.office=offices.id
                        INNER JOIN parties ON candidates.party=parties.id WHERE {}={}""".format(selector, value))
        item = self.cursor.fetchone()
        return item

    def fetch_all_candidates(self, selector, value):
        self.cursor.execute(""" SELECT users.firstname, users.lastname, offices.name, parties.name
                        FROM candidates INNER JOIN users ON candidates.candidate=users.id
                        INNER JOIN offices ON candidates.office=offices.id
                        INNER JOIN parties ON candidates.party=parties.id WHERE {}={}""".format(selector, value))
        item = self.cursor.fetchall()
        return item

    def fetch_all_results(self, id):
        self.cursor.execute("""SELECT offices.name, users.firstname, users.lastname, COUNT(*) as votes FROM votes
                    INNER JOIN offices ON offices.id=votes.office
                    INNER JOIN users ON users.id=votes.candidate WHERE office={}
                    GROUP BY offices.name, users.firstname, users.lastname;""".format(id))
        item = self.cursor.fetchall()
        return item

    def default_admin(self):
        admin = {
            "firstName": "Kipruto",
            "lastName": "Barno",
            "otherName": "Maxwel",
            "email": "admin@politico.com",
            "phoneNumber": "0708344488",
            "passportUrl": "admin.png",
            "isAdmin": True,
            "password": "$pbkdf2-sha256$29000$gvC.1/q/9x7DGKP0fu/dWw$k5fSiU1MK/XHyMbZofnBxrE.OPd.FScTNntfJGwnt48"
        }
        self.cursor.execute(
            """SELECT * FROM users WHERE email='admin@politico.com'""")
        if not self.cursor.fetchone():
            self.insert('users', admin)